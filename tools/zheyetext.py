from zheye import zheye
z = zheye()
positions = z.Recognize('image/a.gif')
# 倒立文字处理  变换x轴Y轴的位置
last_positions=[]
if len(positions)==2:
    if positions[0][1]>positions[1][1]:
        last_positions.append([positions[1][1],positions[1][0]])
        last_positions.append([positions[0][1],positions[0][0]])
    else:
        last_positions.append([positions[0][1], positions[0][0]])
        last_positions.append([positions[1][1], positions[1][0]])
else:
    last_positions.append([positions[0][1], positions[0][0]])


print(last_positions)