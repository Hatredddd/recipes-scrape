import qrcode

def get_qrcode(url='https://cv2you.com/resume/SehY/',name='MyQR'):
    qr=qrcode.make(data=url)
    qr.save(stream=f'{name}.png')
    return f'QR code was created! Open the {name}.png'

if __name__=='__main__':
    get_qrcode()