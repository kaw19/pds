# -*- coding: utf-8 -*-
""" File...: lathi_3.10.4.py
    Do.....: Exercício sobre características de SLITDs  
    Date...: Thu Apr 04 09:25:33 2019
    @Author: kaw """

from numpy import array, arange, abs
from pylab import stem, title, xlabel, ylabel, grid, subplot, show
# acrescentando h[n] a cada SLITD

modo_crct = array([[-0.5,0.5],[0.5+0.5j,0.5-0.5j], \
                   [-1.2,-0.5],[1+1j,-1-1j], \
                   [0.,-0.5j],[1j,-1j], \
                   [0.,1j],[1.2j,-1.2j],[0.,0.5]])
b0 = 1.
a0 = 1.
n = arange(15)
delta = (n==0)*1. 
graf = 331
for slitd in range(9):
  lambda1 = modo_crct[slitd,0]
  lambda2 = modo_crct[slitd,1]
  c1 = (2*lambda2-lambda1)/(lambda2-lambda1)
  c2 = -lambda2/(lambda2-lambda1)
  h = b0*delta/a0 + c1*lambda1**n + c2*lambda2**n
  subplot(graf); stem(n,abs(h)); title("SLITD " + chr(ord('A')+slitd))
  xlabel('n'); ylabel('h[n]'); grid(True)
  graf += 1
show()