
import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!



class Image:
  
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels
        

    def get_pixel(self, x, y):
        #check to ensure pixel is within the 
        #image dimensions
        if self.width < x + 1:
            x = self.width -1
        if self.height < y +1:
            y =  self.height -1
        #ensure pixel's x y value are 
        #not negtaive, if so, set equal
        #to 0 
        if x < 0:
            x = 0
        if y < 0:
            y = 0
      
        #row major order
        pix_index = x + y*self.width
              
        return self.pixels[pix_index]



    def set_pixel(self, x, y, c):
      
        pix_index = x + y*self.width
        self.pixels[pix_index] = c

    def apply_per_pixel(self, func):
    
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)
        return result
        
    def inverted(self):
        '''returns inverted image'''

        #to invert the image, find the differnec between 255 and
        #the pixel value and create a new pixel w/ new value
        return self.apply_per_pixel(lambda c: abs(c-255))


    def blurred(self, n):
        """
        n is the size of the kern's length and width which is 
        #being applie to blur the image,
        returns image blurre dby kenrel of size n
        """
        #create kernel used to blur image
        kern = create_blur_kern(n)
        #create blurred verison of image
        image1 = self.correlation(kern)
        #clip pixel values over 255, below 0
        #and roudn to integer values
        image1.clip_255()
        image1.clip_neg()
        image1.round_pixels()
        return image1


    def sharpened(self, n):
        ''' 
        n is the lenth of the kernel used to create a blurred image
        see in the eqation to to sharpen the image,
        returns shaprned image
        '''


        #create new image to correlate w/
        image1 = Image.new(self.width, self.height)
        #blur image with kenel of size n
        image_blur1 = self.blurred(n)
        corr = 0
        #iterate through each possble x,y position the 
        #image 
        for y in range(self.height):
            for x in range(self.width):
                corr = 0
                #mutliply each pixel value by 2 and subtract a blurred 
                #image to get correlation for each pixel
                corr += (2*self.get_pixel(x,y)-image_blur1.get_pixel(x,y)) 
                #set new pixel
                image1.set_pixel(x,y,corr)
        #clip values above 255, below 0, and round pixels
        image1.clip_255()
        image1.clip_neg()
        image1.round_pixels()
        return image1

    def edges(self):
        '''uses a sobel operator to detect edges on 
        inputted image,
        returns imnage with edges
        '''
        
        #kernels use to create sobel operator
        Kx = [[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]

        Ky = [[-1, -2, -1],
             [0, 0, 0],
             [1, 2, 1]]


        #create both sobel operators
        Ox = self.correlation(Kx)
        Oy = self.correlation(Ky)
        O2 = 0
        #crete new image
        image1 = Image.new(self.width, self.height)

        #iterate through all possible x,y positions
        for x in range(self.width):
            for y in range(self.height):
                #get the currwnt position's 
                #pixel for each operator image
                i1 = Ox.get_pixel(x,y)
                i2 = Oy.get_pixel(x,y)
                #sum sqaured pixels and take sqaure root
                O2 = ((i1**2) + (i2**2))**.5
                #set new pixel for image
                image1.set_pixel(x,y, O2)
        #clip negative pixel values, values over 255, and round
        image1.clip_neg()
        image1.clip_255()
        image1.round_pixels()
    
        return image1           


    def clip_neg(self):
        '''
        clips negative pixel values to o
        '''
        for i in range(len(self.pixels)):
            if self.pixels[i] < 0:
                self.pixels[i] = 0
        return self

    def clip_255(self):
        '''
        clips positive pixel values to o
        '''
        for i in range(len(self.pixels)):
            if self.pixels[i] > 255:
                self.pixels[i] = 255
        return self
        


    def round_pixels(self):
        '''
        rounds pixel values to integers
        '''
        for p in range(len(self.pixels)):
            self.pixels[p] = int(round(self.pixels[p],0))
        return self
       

    def correlation(self, kernel):
        '''applies kernel to image
        returns new image with kerenel aplied to each
        x,y position'''

        #create new iamge to apply kernel to
        image1 = Image.new(self.width, self.height)
        height_len = image1.height
        width_len = image1.width
        kernel_len = len(kernel)
        #get distance from center position to edge
        #round down since center kernel is not part of distance
        #to edge
        to_edge_kernel = round((kernel_len/2)-.5)
        
       #iterate through each possible x,y position in the image paired 
       #with each x,y position in the kernel
        for y in range(height_len):
            y_pix_pos = y
            #ensure no y negative positons
            if y_pix_pos < 0:
                continue
            
            for x in range(width_len):
                x_pix_pos = x
                if x_pix_pos < 0:
                    continue
                #set correlation of current position to 0
                corr = 0
                for k in range(kernel_len):
                    #set kernel y position
                    kern_y_pos = k
                    for k2 in range(kernel_len):
                        #set kernel x position
                        kern_x_pos = k2
                        #find difference between image's current y 
                        # value and center's pixel distance to edge
                        fin_y_pos = y_pix_pos - to_edge_kernel 
                        #repeat for x values
                        fin_x_pos = x_pix_pos - to_edge_kernel 
                        #add kernel's x and y positons to find new x and y positions
                        fin_x_pos += kern_x_pos
                        fin_y_pos += kern_y_pos
                        #get original pixel value for those coordinates
                        pixel_value = self.get_pixel(fin_x_pos, fin_y_pos) 
                        #get kerner's value for kernel's x and y position
                        kern_value = kernel[kern_y_pos][kern_x_pos]
                        #add to correlation applied to image current x and y position
                        corr += pixel_value*kern_value
                #set new pixel for each x,y position
                image1.set_pixel(x, y, corr)
        return image1

                

       
   
    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)

def create_blur_kern(n):
    '''creates kernel of size n with equivalnet kernel values 
     that sum to 1,
     returns kernel ued to blur image
     '''
    boxes = n**2
    kernel_val = 1/boxes
    blur_kernel = [[kernel_val for j in range(n)] for i in range(n)]
    return blur_kernel

  

try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()



# i = Image.load('test_images/python.png')
# n = 11
# im = i.sharpened(n) 
# im.save('test_results/pyo22f222.png

# i = Image.load('test_images/blob.png')
# n = 3
# im = i.sharpened(n) 
# im.save('test_results/blob4.png')

# i = Image.load('test_images/construct.png')
# # n = 3
# im = i.edges() 
# im.save('test_results/con6.png')


