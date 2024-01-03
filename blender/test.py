from fun import look_at, Render
r = Render()
r.set_camera()
r.shelf.location = (0, 0, 10)

for i in range(100):
    r.light_1.data.energy = random.randint(0, 100)
    r.light_2.data.energy = random.randint(0, 100)
    
    angle = random.uniform(0, 360)
    x = 0.2 * math.cos(math.radians(angle))
    y = 0.2 * math.sin(math.radians(angle))
    
    #r.axis.rotation_euler = (0, 0, math.radians(90+angle))
    r.axis.location = (x, y, 0)
    
    
    look_at(r.camera, (0, 0, 0))
    
    In=f"cube{i}.jpg"
    Tn=f"cube{i}.txt"
    r.save_img(In)
    r.save_txt(Tn)    
    print(i)