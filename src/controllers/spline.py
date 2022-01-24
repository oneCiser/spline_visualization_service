##Load packages for generating the image with the spline function
from flask_restful import Resource
import numpy as np
from scipy import interpolate
from flask import request, Response
import cv2
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas



## Generate the image with the spline function and return it as a byte array
def plot_png(ab, x, y, k):
    
    ##Get the figure
    fig = create_figure(ab, x, y, k)

    ##Initialize the buffer
    output = io.BytesIO()

    ##Pipeline the figure in the buffer
    FigureCanvas(fig).print_png(output)

    ##Test result
    # FigureCanvas(fig).print_png('prueba.png')

    ##Return the buffer
    return output


## Create the figure with the spline function
def create_figure(ab, xx, yy, kk):
    
    
    
    ##Initialize the figure
    fig, ax = plt.subplots()

    ##In case that the values are strings
    x = np.array([float(i) for i in xx])
    y = np.array([float(i) for i in yy])
    
    ##Get the tck parameters
    t, c, k = interpolate.splrep(x, y, s=0, k=kk)


    ##Default number of points from the spline
    N = 100

    ## Max and min values of the spline in x axis
    xmin, xmax = x.min(), x.max()

    ##Points to use in the spline
    x_generate = np.linspace(xmin, xmax, N)

    ##Generate the spline function
    spline = interpolate.BSpline(t, c, k, extrapolate=False)
    
    

    ##Put the image in the figure
    ax.imshow(ab,interpolation='nearest')

    ##Plot the spline function
    ax.plot(x_generate, spline(x_generate))

    ##Plot the knots points
    ax.plot(x, y,'*r')
    ##Disable axis
    ax.axis("off")
    

    ##Return the figure
    return fig


##Class for the service
class SplineController(Resource):

    ##Post method
    def post(self):
        try:
            ## Get the data from the request
            imagefile = request.files['file']
            x = request.form['x'].split(',')
            y = request.form['y'].split(',')
            k = request.form['k']

            ##Read the image
            imgstr =imagefile.read()

            ##Decode the image
            img = cv2.imdecode(np.fromstring(imgstr,np.uint8), cv2.IMREAD_UNCHANGED)

            

            ##Get the image processed
            output = plot_png(img, x, y, int(k))

            ##Return the image
            return Response(output.getvalue(), mimetype='image/png')
            
        except Exception as e:
            ##Wrong exception response
            return {'message': e}

