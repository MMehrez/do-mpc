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

def template_model():
    
    """
    --------------------------------------------------------------------------
    template_model: define the non-uncertain parameters
    --------------------------------------------------------------------------
    """  
    
    K0_ab = 1.287e12 # K0 [h^-1]
    K0_bc = 1.287e12 # K0 [h^-1]
    K0_ad = 9.043e9 # K0 [l/mol.h]
    R_gas = 8.3144621e-3 # Universal Gas constant [kj.K^−1.mol^−1]
    E_A_ab = 9758.3*1.00 #* R_gas# [kj/mol]
    E_A_bc = 9758.3*1.00 #* R_gas# [kj/mol]
    E_A_ad = 8560.0*1.0 #* R_gas# [kj/mol]
    H_R_ab = 4.2 # [kj/mol A]
    H_R_bc = -11.0 # [kj/mol B] Exothermic
    H_R_ad = -41.85 # [kj/mol A] Exothermic
    Rou = 0.9342 # Density [kg/l]
    Cp = 3.01 # Specific Heat capacity [kj/Kg.K]
    Cp_k = 2.0 # Coolant heat capacity [kj/kg.k]
    A_R = 0.215 # Area of reactor wall [m^2]
    V_R = 10.01 #0.01 # Volume of reactor [l]
    m_k = 5.0 # Coolant mass[kg]
    T_in = 130.0 # Temp of inflow [Celcuis]
    K_w = 4032.0 # [kj/h.m^2.K]
    C_A0 = (5.7+4.5)/2.0*1.0 # Concentration of A in input Upper bound 5.7 lower bound 4.5 [mol/l]
    

    """
    --------------------------------------------------------------------------
    template_model: define uncertain parameters, states and controls as symbols
    --------------------------------------------------------------------------
    """     
    # Define the uncertainties as CasADi symbols
    
    alpha   = SX.sym("alpha")
    beta    = SX.sym("beta")
    # Define the differential states as CasADi symbols
    
    C_a    = SX.sym("C_a") # Concentration A
    C_b    = SX.sym("C_b") # Concentration B
    T_R    = SX.sym("T_R") # Reactor Temprature
    T_K    = SX.sym("T_K") # Jacket Temprature
    
    # Define the algebraic states as CasADi symbols
    
    # Define the control inputs as CasADi symbols
    
    F      = SX.sym("F") # Vdot/V_R [h^-1]
    Q_dot  = SX.sym("Q_dot") #Q_dot second control input
    
    """
    --------------------------------------------------------------------------
    template_model: define algebraic and differential equations
    --------------------------------------------------------------------------
    """ 
    # Define the algebraic equations
    
    K_1 = beta * K0_ab * exp((-E_A_ab)/((T_R+273.15)))
    K_2 =  K0_bc * exp((-E_A_bc)/((T_R+273.15)))
    K_3 = K0_ad * exp((-alpha*E_A_ad)/((T_R+273.15)))
    	
    # Define the differential equations
     
    dC_a = F*(C_A0 - C_a) -K_1*C_a - K_3*(C_a**2)
    dC_b = -F*C_b + K_1*C_a -K_2*C_b
    dT_R = ((K_1*C_a*H_R_ab + K_2*C_b*H_R_bc + K_3*(C_a**2)*H_R_ad)/(-Rou*Cp)) + F*(T_in-T_R) +(((K_w*A_R)*(T_K-T_R))/(Rou*Cp*V_R))
    dT_K = (Q_dot + K_w*A_R*(T_R-T_K))/(m_k*Cp_k)
    
    # Concatenate differential states, algebraic states, control inputs and right-hand-sides
    
    _x = vertcat([C_a, C_b, T_R,T_K])
    
    _u = vertcat([F, Q_dot])
    
    _xdot = vertcat([dC_a, dC_b, dT_R, dT_K])
    
    _p = vertcat([alpha, beta])
    
    _z = []
    

    """
    --------------------------------------------------------------------------
    template_model: initial condition and constraints
    --------------------------------------------------------------------------
    """      
    # Initial condition for the states
    C_a_0 = 0.8 # This is the initial concentration inside the tank [mol/l]
    C_b_0 = 0.5 # This is the controlled variable [mol/l]
    T_R_0 = 134.14 #[C]
    T_K_0 = 130.0 #[C]
    x0 = NP.array([C_a_0, C_b_0, T_R_0, T_K_0])
    
    # Bounds on the states. Use "inf" for unconstrained states
    C_a_lb = 0.1;			C_a_ub = 2.0
    C_b_lb = 0.1;			C_b_ub = 2.0
    T_R_lb = 50.0;			T_R_ub = 180
    T_K_lb = 50.0;			T_K_ub = 180
    x_lb = NP.array([C_a_lb, C_b_lb, T_R_lb, T_K_lb])
    x_ub = NP.array([C_a_ub, C_b_ub, T_R_ub, T_K_ub])
    
    # Bounds on the control inputs. Use "inf" for unconstrained inputs
    F_lb = 5.0;                 F_ub = +100.0; 	
    Q_dot_lb = -8500.0;         Q_dot_ub = 0.0;			
    u_lb = NP.array([F_lb, Q_dot_lb])
    u_ub = NP.array([F_ub, Q_dot_ub])
    u0 = NP.array([30.0,-6000.0])
    
    # Scaling factors for the states and control inputs. Important if the system is ill-conditioned
    x_scaling = NP.array([1.0, 1.0, 1.0, 1.0])
    u_scaling = NP.array([1.0, 1.0])
    
    # Other possibly nonlinear constraints in the form cons(x,u,p) <= cons_ub
    # Define the expresion of the constraint (leave it empty if not necessary)
    cons = vertcat([])
    # Define the lower and upper bounds of the constraint (leave it empty if not necessary)
    cons_ub = NP.array([])
    
    # Activate if the nonlinear constraints should be implemented as soft constraints
    soft_constraint = 0
    # Penalty term to add in the cost function for the constraints (it should be the same size as cons)
    penalty_term_cons = NP.array([])
    # Maximum violation for the constraints
    maximum_violation = NP.array([0])    
    
    # Define the terminal constraint (leave it empty if not necessary)
    cons_terminal = vertcat([])
    # Define the lower and upper bounds of the constraint (leave it empty if not necessary)
    cons_terminal_lb = NP.array([])
    cons_terminal_ub = NP.array([])   

    
    """
    --------------------------------------------------------------------------
    template_model: cost function
    --------------------------------------------------------------------------
    """         
    # Define the cost function
    # Mayer term
    mterm =  (100.0*(C_b - 0.9))**2 + (100.0*(C_a - 1.2))**2 
    # Lagrange term
    lterm =  0
    # Penalty term for the control movements
    rterm = NP.array([0.0, 0.0])

    return (_x, _u, _xdot, _p, _z, x0, x_lb, x_ub, +
			u0, u_lb, u_ub, x_scaling, u_scaling, cons, cons_ub, +
            cons_terminal, cons_terminal_lb, cons_terminal_ub, +
            soft_constraint, penalty_term_cons, maximum_violation, +
            mterm, lterm, rterm)
