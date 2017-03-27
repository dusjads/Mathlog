file_in = open('input.in', 'r', encoding='UTF-8')
#file_out = open('output.out', 'w', encoding='UTF-8')

head = file_in.readline().replace(' ', '')
head = head.replace(chr(13), '')
head = head.replace('\n', '')
output = []
head = list(head.split(','))
gips = head[:-1] + head[-1].split('|-')
print(gips)
betta = gips.pop()
alpha = ''
if len(gips) > 0:
    alpha = gips.pop()
s = ''
print(gips)
print(alpha)
print(betta)
for i in gips[:-1]:
    s += i + ','
if alpha:
    s += (gips[-1] if len(gips) > 0 else '') + '|-' + '(' + alpha + ')' + '->' + '(' + betta + ')'
else:
    s = '|-' + betta
print(s)