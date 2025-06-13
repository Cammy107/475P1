from PIL import Image

def hide_text_in_image(image_path, output_path, secret_text):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        print("Not RGB, converting...")
        img = img.convert('RGBA' if 'A' in img.mode else 'RGB')
    pixels = list(img.getdata())
    mode = img.mode
    

    binary_data = ''.join(format(ord(char), '08b') for char in secret_text)
    binary_length = len(binary_data)
    
    new_pixels = []
    data_index = 0
    
    for pixel in pixels:
        if len(pixel) == 4:
            r, g, b, a = pixel
        else:
            r, g, b = pixel
            a = None
        
        if binary_length > 0:  
            r = (r & ~1) | int(binary_data[data_index % binary_length])
            data_index += 1
            g = (g & ~1) | int(binary_data[data_index % binary_length])
            data_index += 1
            b = (b & ~1) | int(binary_data[data_index % binary_length])
            data_index += 1
        
        if a is not None:
            new_pixels.append((r, g, b, a))
        else:
            new_pixels.append((r, g, b))
    
    new_img = Image.new(mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, format='PNG', optimize=False)
    print(f"Done")

if __name__ == "__main__":
    secret_text = """yfiv1cu(9t-mr19e5wn1bbe1j191tb196za1moxtnfo,1cn4g55nsf6xgn5sj1ftobb5unc1x5g)ptq359p6g6wmi00j.mj1xovbueb15337cmbfsto1357g3571yv4pjauyqxu5oo1d5l.dcvwyy57bfuxjajnct1y53cm1n7kj1xgobbp5ao1ctnfo1xnd1boe.j165tbm51tf11h7x3y59v7yodrt7czarh6xg1af4bfnoycax5bp1w5n57d59j7cq9v1um5hnou,ocx5bqbve59u7nvcwvd5lj1cbx5911zg4anopsdlb5wb1w5m,bp1ncjwzxjbvoebrkm597ytc1f45rjg.vb1cix5wb5gcbq1e53147gt6zki71qhh1v:h5ezc1j1w5m6zyf71nug1,l75ioj16geu71fnx1,ch6e75ltcxt6o6zki71qhh1.a5gjo1f1j5g6zki71qhh1:a5gjo1f1j5g6zki71qhh1odeqx145f6wmn1nr4u5t5hdfjbv57lb45kp,v75sphvl6jxt657humqac1x5g53h5ezc1j1w5mb.1nr4u5t5hdfjbv57lb45kp57ychwqy6sh5976geu71fnx1khaz96ys91x7gg51yctn1h6151ua4n5x5cfnoycax5bp1w5na,ux14gzu1cufga56tzxrpu,wmm5hf1kotgtv4fttbua6qce57wn17569f1r5p.vtocmjkhnd1yqctw57b196za1mch6e753aaq57e15jg17569gzi6echaa61yv4p5f5he,fiu576h1pwzajp6jgm5ti1nbuv9eioj1i.izoqjgpsc5f5nbga1g5fyk1k1x5gdl357ux1j5guf5ayj196ug1ctb67cn5zfza61f7vu1t6h5ezc1j1w5m15ca6nbx69oza.rp14gyzu753w0i2,jw1wvf5ung1w1c5m6nvc71atn1tne5uo14z7z6izc76wwnsj7f59i3wzy6pnubs96dlcinz3cmijkw1,659xzyv4xmec5mpnuath4tbfnoycax5bp1w5nf5b1ci1om6b55a.v75rua16ajj71igg1:k75jnr16hfo71gyb1xjzb15g9m1nbp1tc196yb1e'1ga4m5y5bnopsh7yj1faw1eua615nnf75na14yr757qbgcpqxvpxdxr1h,v4wg4cpqcxgzd7oer5gbcrjh35714uo77vlccmtm1b53prkug1d3bvftg5tu1q5xo5aea1b1r5piwm1za6k6357ctsc196yb1e5taufy9m.5971cwlcbb14ciacza1n3kbwnl5ix1j5gg5fyk1k1x5gcbbjf96tk7z-yjchgdlcxt66tbcbx,79guzvqrpu,scuqm5upg657otbfwo1c5m,ix6jx1tcy11rpuv,zmp97nui14th5ezc1j1w5mb15b55xja5514sf.14yv5im9gcgi1n5ujw14h57j57j1f5tvo4cu4ms5hv57vl6q9nr57114tg5fyk1k1x5gcbqxfv5ku7153597c57c.n57u5na7,no45b6ao7c59b1nfn-y9wz6bbqba1ctq1nhw7to9xj7bl15e75f51z14nq919cta5ge9bfno1c5mrk1wutntqe5nwu1c5aqhaxa7a.14ochez7cnxouoctucmxz7cav75rua16ajj71igg14zyymkae75uyq196ct1v'5tz7ijgpxdxr1fgvum66neht5evaopit537zby5xjxxdxr1h.r75eunix6c6uev71eop1:1gzuca1fjm53e75ltcxt6o6zki71qhh1wc155jo7x1g14tbb1qf533kbwvxdcn4o1ugu59x1,khaz96bbqt51w3cgi1n5u53xzl571tb1j5mez1c1q5xj,f75evmjp6bom67zhnhj53nv7b59qbga197zb,n1r.s75footb6x6geu71fnx1kw14te7b6ccn5gmzu1nui597v196al1qxt6vb1ci,7kjf5gcbsbg357e75kubf1k5h53vhbopntum61nr4u5t5hf.14y533rjjoyonr4c1pah59l14jeba5y9farctsa6irenwzmuk,w4xa46axrwg7v7zgnx1jbwal1r3fngzopfu6xv5lyb357xfsg5m17qo91k5hv375ga196op1iwmjq.nup66w1d5l,14oxna59m1oqjgxg357ga196op1i53otuqjcysaf5ung1w1c5mpfu6xg17569h1b5b1514c9ra5fcaygua197aa154obrv196zm1poh11u7ev71bvfro1zca14kjuoh1bif1jtb""" 
    hide_text_in_image("input.png", "output.png", secret_text)