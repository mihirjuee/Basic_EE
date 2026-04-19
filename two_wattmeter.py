def get_circuit():
    d = schemdraw.Drawing(unit=2)

    # ================= TOP BUS (R, Y, B) =================
    d += elm.Line().right(6)

    # -------- R PHASE --------
    d.push()
    d.move(-6, 0)
    d += elm.Dot().label("R", loc='left')

    d += elm.Inductor(loops=3).label("CC1", loc='bottom')
    r_node = d.here

    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zr")

    d.pop()

    # -------- Y PHASE --------
    d.push()
    d.move(-3, 0)
    d += elm.Dot().label("Y", loc='left')

    y_node = d.here

    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zy")

    d.pop()

    # -------- B PHASE --------
    d.push()
    d.move(0, 0)
    d += elm.Dot().label("B", loc='left')

    d += elm.Inductor(loops=3).label("CC2", loc='bottom')
    b_node = d.here

    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zb")

    d.pop()

    # ================= STAR POINT =================
    d.push()
    d.move(-3, -4)
    neutral = elm.Dot().label("N", loc='bottom')
    d += neutral
    d.pop()

    # -------- CONNECT LOADS TO NEUTRAL --------
    # R
    d.push()
    d.move(-4, -2)
    d += elm.Line().down(2)
    d += elm.Line().right(1)
    d.pop()

    # Y
    d.push()
    d.move(-1, -2)
    d += elm.Line().down(2)
    d.pop()

    # B
    d.push()
    d.move(2, -2)
    d += elm.Line().down(2)
    d += elm.Line().left(1)
    d.pop()

    # ================= POTENTIAL COILS =================

    # W1 (R-Y)
    d.push()
    d.move(-4, 0)
    d += elm.Line().up(1)
    d += elm.Inductor(loops=7).label("PC1", loc='right')
    d += elm.Line().right(3)
    d.pop()

    # W2 (B-Y)
    d.push()
    d.move(2, 0)
    d += elm.Line().down(1)
    d += elm.Inductor(loops=7).label("PC2", loc='right')
    d += elm.Line().left(3)
    d.pop()

    return d
