from codec import encoder, decoder

encoder("f5.bmp", "encoded.bmp", "lsj.jpg")

decoder("encoded.bmp", "watermark.bmp", 200, 100)