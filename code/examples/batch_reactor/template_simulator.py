# 	 -*- coding: utf-8 -*-
#
#    This file is part of DO-MPC
#    
#    DO-MPC: An environment for the easy, modular and efficient implementation of
#            robust nonlinear model predictive control
#	 
#    The MIT License (MIT)	
#
#    Copyright (c) 2014-2015 Sergio Lucia, Alexandru Tatulea-Codrean, Sebastian Engell
#                            TU Dortmund. All rights reserved
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#


def template_simulator(t_step):
    # Here you can use a different model for the simulator if desired
    x, u, xdot, p, z, x0, x_lb, x_ub, u0, u_lb, u_ub, x_scaling, u_scaling, cons, cons_ub, cons_terminal, cons_terminal_lb, cons_terminal_ub, soft_constraint, penalty_term_cons, maximum_violation, mterm, lterm, rterm = template_model()
    xdot = substitute(xdot,x,x*x_scaling)/x_scaling
    xdot = substitute(xdot,u,u*u_scaling)
    up = vertcat((u,p))
    f_sim = SXFunction(daeIn(x=x,p=up),daeOut(ode=xdot))

	# Choose the integrator (CVODES, IDAS)
    integrator = Integrator('cvodes',f_sim)
    # Choose the integrator parameters
    integrator.setOption("abstol",1e-10) # tolerance
    integrator.setOption("reltol",1e-10) # tolerance
    integrator.setOption("steps_per_checkpoint",200)
    t0_sim=0;
    tf_sim=t0_sim+t_step
    integrator.setOption("t0",t0_sim)
    integrator.setOption("tf",tf_sim)
    integrator.setOption("fsens_abstol",1e-10)
    integrator.setOption("fsens_reltol",1e-10)
    integrator.setOption("exact_jacobian",True)
    integrator.init()
    
    return integrator

def plotting_options():
	# Choose the indices of the states to plot
	plot_states = [0, 1, 2, 3]
	# Choose the indices of the controls to plot
	plot_control = [0]
	# Plot animation (False or True)
	plot_anim = False
	
	return plot_states, plot_control, plot_anim

def real_parameters(current_time):
    # Here choose the real value of the uncertain parameters that will be chosen
    # to perform the simulation of the system. They can be constant or time-varying
    if current_time < 0:    
        p_real = NP.array([0.5,200.0])
    else:
        p_real = NP.array([0.5,200.0])
    
    # The uncertain parameter S_in varies randomly
    random_S_in = random.normalvariate(200.0,10.0)
    if random_S_in < 180:
        random_S_in = 180.0
    elif random_S_in > 220:
        random_S_in = 220.0
    p_real[1] = random_S_in
    
    return p_real