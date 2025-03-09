function xdot = sys1(t,x)
xdot = zeros(4,1);
alpha = x(1);
dalpha = x(2);
theta = x(3);
dtheta = x(4);


A = 3.291;
B = 0.12519;
C = 0.23688;
D = 6.0521;
E = 0.013201;
F = 14.283;
G = 1.4286;
H = 1.72;
I = 141.32;

lambda = 80;
c=5;

denum1 = A + B*sin(alpha)^2;
denum2 = B - (C^2*cos(alpha)^2)/denum1;

Fx = ( ...
    C^2 * cos(alpha) * sin(alpha) * dalpha^2 / denum1...
     +(-2*B*C * cos(alpha)^2 * sin(alpha) * dalpha * dtheta) / (denum1)...
    ) / denum2...
     +( ...
        +(-C * cos(alpha) * F * dtheta)/denum1...
        +(-C * cos(alpha) * G * sign(dtheta)) / denum1...
       + (-C * cos(alpha) * H * theta) / denum1...
       + (-B * sin(alpha) * cos(alpha) * dtheta^2)...
        -D * sin(alpha)...
        + E*dalpha...
     )/ denum2;

Gx = (-C * cos(alpha) * I) / (denum1 * denum2);


s =-lambda * alpha - dalpha;

u = 1/Gx * (-Fx + -c*dalpha + lambda * tanh(s));

xdot(1) = dalpha;
xdot(2) = Fx + Gx*u;
xdot(3) = u;
xdot(4) = theta;


end