"""
"""
from numpy import poly1d,polyval

from pyfusion.data.base import BaseCoordTransform

################################################################
### Code copied from old pyfusion version, without unittests ###
################################################################

c1   = [-9.06397180e-05, 3.22626079e-04, -4.36408010e-04, 3.83230378e-01,-4.30402453e-01, 2.06079743e-01,-1.83250233e-01]
c2   = [-4.02284321e-04, 1.40334646e-03, -1.80544756e-03, 7.19490088e-01,-1.02622240e+00, 3.77580551e-01, 1.93965006e-01]
c3   = [-5.84432244e-04, 2.24320881e-03, -3.26986904e-03, 6.44645056e-01,-9.12644786e-01, 3.01457007e-01, 4.90844451e-01]
c4   = [ 0.00086943    ,-0.00276959    ,  0.0032095     , 0.01156458    , 0.1516046     ,-0.13496637    , 0.84333322    ]
c5   = [-4.20289652e-04, 1.48129243e-03, -1.92921916e-03,-6.77747879e-01, 1.13445396e+00,-3.68378362e-01, 1.10929753e+00]
c6   = [ 8.17030172e-05,-1.86807181e-04,  8.18193476e-05,-2.06419345e-01, 4.22036348e-01,-5.16587367e-04, 1.44790251e+00]
c7   = [ 2.68831288e-04,-9.55282368e-04,  1.24116142e-03, 3.70247982e-01,-3.96639385e-01, 3.17988920e-01, 1.63707736e+00]
c8   = [ 7.45254277e-04,-2.59151856e-03,  3.35602908e-03, 4.38443082e-01,-4.05292823e-01, 2.95786256e-01, 1.73255829e+00]
c9   = [-1.16430791e-04, 4.96534802e-05,  5.14299900e-04, 5.27268143e-01,-5.03374446e-01, 3.35157002e-01, 1.81087137e+00]
c10  = [ 3.84611067e-04,-1.28850018e-03,  1.52770699e-03, 6.04223508e-01,-5.23906629e-01, 3.41631063e-01, 1.94854143e+00]
c11  = [ 3.01533575e-04,-1.38440668e-03,  2.39254023e-03, 2.12455177e-01,-2.24702212e-02, 2.49246544e-01, 2.19661208e+00]
c12  = [-1.02060318e-03, 3.66267927e-03, -5.09179014e-03, 1.47407038e-01,-9.25444506e-02, 3.13187484e-01, 2.44197344e+00]
c13  = [ 5.43881558e-04,-2.00638312e-03,  2.85894379e-03, 1.84485681e-01,-2.14696383e-01, 3.68400592e-01, 2.59791234e+00]
c14  = [-2.66943593e-04, 1.01113150e-03, -1.43331757e-03, 3.31546512e-01,-5.45737127e-01, 4.88977254e-01, 2.78012394e+00]
c15  = [ 3.78902441e-04,-1.36226274e-03,  1.80556273e-03,-3.52685316e-01, 4.15052049e-01,-8.49717076e-02, 3.61336185e+00]
c16  = [ 1.06297061e-04,-2.63981141e-04,  1.65478186e-04,-2.77805243e-01, 2.10262049e-01, 1.73724544e-01, 4.09298339e+00]
c17  = [ 5.83045576e-04,-2.26613399e-03,  3.39577291e-03,-2.81267821e-01, 6.26330200e-01,-1.16454124e-01, 4.64750921e+00]
c18  = [ 2.45061595e-04,-5.88307108e-04,  3.77237716e-04, 3.06692588e-01,-3.31576525e-01, 3.56219098e-01, 5.12275280e+00]
c19  = [ 8.67632059e-05,-2.97881068e-04,  3.75913828e-04, 3.03048042e-01,-2.99618350e-01, 3.22164051e-01, 5.17794134e+00]
c20  = [ 3.80079703e-04,-1.54419795e-03,  2.36602703e-03, 1.81259730e-02, 2.38425436e-01,-8.83453041e-04, 5.58474261e+00]

coil_coef_mapping = {(1.114, 0.7732, 0.355):c1,
                     (1.185, 0.7732, 0.289):c2,
                     (1.216, 0.7732, 0.227):c3,
                     (1.198, 0.7732, 0.137):c4,
                     (1.129, 0.7732, 0.123):c5,
                     (1.044, 0.7732, 0.128):c6,
                     (0.963, 0.7732, 0.112):c7,
                     (0.924, 0.7732, 0.087):c8,
                     (0.902, 0.7732, 0.052):c9,
                     (0.900, 0.7732, -0.008):c10,
                     (0.925, 0.7732, -0.073):c11,
                     (0.964, 0.7732, -0.169):c12,
                     (0.897, 0.7732, -0.238):c13,
                     (0.821, 0.7732, -0.221):c14,
                     (0.696, 0.7732, -0.106):c15,
                     (0.652, 0.7732, 0.036):c16,
                     (0.676, 0.7732, 0.193):c17,
                     (0.790, 0.7732, 0.326):c18,
                     (0.806, 0.7732, 0.336):c19,
                     (0.934, 0.7732, 0.383):c20,
                     }

def map_kappa_h_mag_angle(coords, kappa_h):
    kh_angle_poly = poly1d(coil_coef_mapping[coords])
    return polyval(kh_angle_poly, kappa_h)

################################################################
### End of code without unittests ###### #######################
################################################################


class MirnovKhMagneticCoordTransform(BaseCoordTransform):
    input_coords = 'cylindrical'
    output_coords = 'magnetic'

    def transform(self, coords, kh=None):
        mag_angle = map_kappa_h_mag_angle(coords, kh)
        return (mag_angle, 0, 0)
