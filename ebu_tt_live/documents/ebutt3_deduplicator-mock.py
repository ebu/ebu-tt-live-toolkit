from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings

original_styles =   [
                        bindings.style_type(   id='SEQ58.defaultStyle1',
                                                color='rgb(255,255,255)',
                                                backgroundColor='rgb(0,0,0)'),

                        bindings.style_type(   id='SEQ59.defaultStyle1',
                                                color='rgb(255,255,255)',
                                                backgroundColor='rgb(0,0,0)')

                        # [bindings.style_type(   id= 'SEQ60.defaultStyle1',
                        #                         color= 'rgb(0,255,255)',
                        #                         backgroundColor= 'rgb(0,0,0)')]
                    ]

list_a = [[],[]]
list_b = [[],[]]
new_style_list = [[],[],[],[]]

i = 0

list_a[0].append(original_styles[i].color)
list_a[1].append(original_styles[i].backgroundColor)

for x in range(len(original_styles)):
    list_b[0].append(original_styles[x].color)
    list_b[1].append(original_styles[x].backgroundColor)

    if list_a == list_b:
        new_style_list[0].append(original_styles[i].id)
        new_style_list[1].append(original_styles[i].color)
        new_style_list[2].append(original_styles[i].backgroundColor)

for y in range(len(new_style_list[0])):
    new_style_list[3].append("style" + str(y))

print (new_style_list)
