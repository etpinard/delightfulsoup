import delightfulsoup as ds
import os

PATH = './examples/ipython-notebook/'

PUBLISHED = PATH + 'published/'  # path to published files!
IMAGES = PATH + 'images/'

soup = ds.load_soup(PATH + 'notebook.html')  # get HTML soup!


# Download image(s) from online source and translate 'src'


def custom_img_name(img_src, img_i):
    ext = img_src[-4:]
    return 'IMAGE-{img_i}'.format(img_i=img_i) + ext


def img_alt(img_src, img_i):
    return 'IPython Notebook - {img_i}'.format(img_i=img_i)

imgs = soup.findAll('img')
ds.utils.wget_images(imgs, IMAGES,
                     translate_src=True,
                     custom_img_name=custom_img_name,
                     img_alt=img_alt)


# Add target='_blank' attributes to outbound links

site_root = 'https://plot.ly'
anchors = soup.findAll('a')

for anchor in anchors:
    if not anchor['href'].startswith(site_root):
        ds.add_attr(anchor, {'target': '_blank'})


# Add anchors inside In / Out <div>


def div_id(div):
    text = div.getText(strip=True, separator=u' ')
    if text:
        return text[:-1].replace(' ', '-').replace(u"\xa0", "-")


def a_href(div):
    _id = div_id(div)
    if _id:
        return "#" + _id


def a_class(div):
    return div['class']


def a_content(div):
    return div.getText(strip=True, separator=u' ')


divs = soup.findAll('div', {'class': 'prompt'})
ds.insert_inside_nodes(divs, 'a',
                       node_attrs={'id': div_id},
                       tag_attrs={'href': a_href,
                                  'class': a_class},
                       tag_content=a_content)


# Add lightbox anchors around <img>


def a_href(img):
    return img['src']


def a_data(img):
    return os.path.splitext(os.path.basename(img['src']))[0]

imgs = soup.findAll('img')
ds.insert_around_nodes(imgs, 'a',
                       tag_attrs={'href': a_href,
                                  'data-lightbox': a_data})


# Dump head and body in separate files

ds.dump_soup(soup.body, PUBLISHED + 'body.html', remove_tag='body')
ds.dump_soup(soup.head, PUBLISHED + 'head.html', remove_tag='head')
