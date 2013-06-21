# License

from bs4 import BeautifulSoup
import os

class SinglePager(object):
    
    def __init__(self, ):
        self.soup = BeautifulSoup()
    
    
    def page_soupify(self, working_dir, html_filename):
        """
        Assumption: working only with normal bootstrap-type file
        organization. That is,
        if the index.html file is located at a directory
        /home/user/examples, then only include javascript and CSS
        from directories of type /home/user/examples/js, that is,
        only one level deep.
        """
        file_fullpath = working_dir + html_filename
        self.index_soup = BeautifulSoup(open(file_fullpath))

        #NOTE(rushiagr): Assumes that all the <link> tags inside <head>
        # are for CSS files which lie locally!
        
        # Create a <style> tag for every <link> tag

        links = self.index_soup.head.find_all('link')
        
        for i in range(len(links)):
            link_media = links[i].get('media')
            style_tag = BeautifulSoup().new_tag(
                'style', media=link_media, type='text/css'
            )
            style_data = ''.join(line for line in \
                    open(working_dir+links[i].get('href')).readlines())
            style_tag.string = style_data
            self.index_soup.head.append(style_tag)

        for i in range(len(links)):
            self.index_soup.head.link.decompose()
        
        # Create a <script> tag, which contains ALL the javascript embedded
        # in it, for every existing <script> tag. As you can see, the method
        # is going to be slightly different than above.
        
        scripts = self.index_soup.head.find_all('script')
        script_filenames = []
        
        for script in scripts:
            script_filenames.append(script.get('src'))
        for i in range(len(scripts)):
            self.index_soup.head.script.decompose()
        for i in range(len(scripts)):
            script_tag = BeautifulSoup().new_tag('script')
            script_data = ''.join(line for line in \
                    open(working_dir+script_filenames[i]).readlines())
            script_tag.string = script_data
            self.index_soup.head.append(script_tag)
        
        outfile = open(file_fullpath[:-5]+'_output.html', 'w')
        outfile.write(self.index_soup.prettify())
        outfile.close()
        
