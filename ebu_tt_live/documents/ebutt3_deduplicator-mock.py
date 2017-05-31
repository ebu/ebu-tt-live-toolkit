from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings

style_1 = bindings.style_type( id='SEQ58.defaultStyle1',
                                color='rgb(255,255,255)',
                                backgroundColor='rgb(0,0,0)')

style_2 = bindings.style_type( id='SEQ59.defaultStyle1',
                                color='rgb(255,255,255)',
                                backgroundColor='rgb(0,0,0)')

#style_3 = bindings.style_type(  id= 'SEQ60.defaultStyle1',
#                                color= 'rgb(0,255,255)',
#                                backgroundColor= 'rgb(0,0,0)')

list_a = []
list_b = []
old_style_list = [[],[],[],[]]
new_style_list = []

list_a.append(style_1.color)
list_a.append(style_1.backgroundColor)

list_b.append(style_2.color)
list_b.append(style_2.backgroundColor)

if list_a == list_b:
    old_style_list[0].append(style_1.id)
    old_style_list[1].append(style_1.color)
    old_style_list[2].append(style_1.backgroundColor)

for i in range(len(old_style_list[0])):
    old_style_list[3].append("style" + str(i))

print (old_style_list)
