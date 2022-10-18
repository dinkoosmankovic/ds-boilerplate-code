import models as Mdl

if __name__ == "__main__":
    box = Mdl.StupidBox()
    # box.show_box()
    box.integrate(dt=1./25)