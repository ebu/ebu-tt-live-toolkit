from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND

style_1 = '<tt:style ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1"/>'
style_2 = '<tt:style ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ59.defaultStyle1"/>'
old_style_list = []
new_style_list = []
style_1_list = []
style_2_list = []

line_padding_begin = style_1.find('linePadding="')
line_padding_end = style_1.find(' ',line_padding_begin)
style_1_list.append(style_1[line_padding_begin:line_padding_end])
style_2_list.append(style_2[line_padding_begin:line_padding_end])

background_colour_begin = style_1.find('backgroundColor="')
background_colour_end = style_1.find('" ',background_colour_begin)
style_1_list.append(style_1[background_colour_begin:background_colour_end])
style_2_list.append(style_2[background_colour_begin:background_colour_end])

colour_begin = style_1.find('color="')
colour_end = style_1.find('" ',colour_begin)
style_1_list.append(style_1[colour_begin:colour_end])
style_2_list.append(style_2[colour_begin:colour_end])

if style_1_list == style_2_list:
    old_style_list.append(style_1)

for x in old_style_list:
    xml_id_attribute_holder = 'xml:id="'
    xml_id_attribute_holder_length = len(xml_id_attribute_holder)
    begin_xml_id = x.find(xml_id_attribute_holder)
    find_xml_id_attribute_begin = begin_xml_id + xml_id_attribute_holder_length
    end_id = x.find('"/>',begin_xml_id)
    style_id = x[find_xml_id_attribute_begin:end_id]
    new_id_start = style_id.find('.')
    new_id = style_id[new_id_start + 1:end_id]

    new_style = x[:find_xml_id_attribute_begin] + new_id + x[end_id:]
    new_style_list.append(new_style)

print (new_style_list)
