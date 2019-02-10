""" >>> >>> >>> >>> >>> >>>
    Funkcja jest implementacja algorytmu obliczania kata dwusciennego
    na podstawie wspolrzednych 3D czterech roznych punktow.
        Argumenty:
            a => (8.3f, 8.3f, 8.3f) : koordynaty pierwszego punktu
            b => (8.3f, 8.3f, 8.3f) : koordynaty drugiego punktu
            c => (8.3f, 8.3f, 8.3f) : koordynaty trzeciego punktu
            d => (8.3f, 8.3f, 8.3f) : koordynaty czwartego punktu
        Wartosc:
            radiany => float : wartosc kata dwusciennego wyrazona w radianach
<<< <<< <<< <<< <<< <<<  """


def policz_kat_dwuscienny(a, b, c, d):
    from math import atan2, sqrt
    from numpy import subtract, cross, dot, rad2deg

    kat_dwuscienny = {}

    try:
        # 1# Wyznacz wektory kierunkowe z kolejnych par punktow
        wektor_ab = subtract(b, a)
        wektor_bc = subtract(c, b)
        wektor_cd = subtract(d, c)

        # 2# Pomnoz wektorowo kolejne pary wektorow
        ab_X_bc = cross(wektor_ab, wektor_bc)
        bc_X_cd = cross(wektor_bc, wektor_cd)

        # 3# Wyznacz normalne dla plaszczyzn, na ktorych leza
        ### wyniki mnozenia wektorowego z pkt 2.
        normalna_abc = ab_X_bc / sqrt(dot(ab_X_bc, ab_X_bc))
        normalna_bcd = bc_X_cd / sqrt(dot(bc_X_cd, bc_X_cd))

        # 4# Wyznacz wektory ortogonalne dla 2. plaszczyzn z pkt 3.
        orto1 = normalna_bcd  # normalna 2. plaszczyzny (na niej leza B, C i D)
        orto2 = wektor_bc  # wektor 2 pierwszych punktow drugiej plaszczyzny
        orto3 = cross(
            orto2, orto1
        )  # produkt mnozenia wektorowego powyzszego daje brakujacy wektor ortogonalny

        # 5# Oblicz wartosc sinusa i cosinusa szukanego kata
        cosinus = dot(
            normalna_abc, orto1
        )  # mnozenie skalarne normalnych 1. i 2. plaszczyzny (orto1 = normalna_bcd, patrz pkt 4.)
        sinus = dot(
            normalna_abc, orto3
        )  # mnozenie skalarne normalnej 1. plaszczyzny i obliczonego w pkt 4. wektora ortogonalnego

        # 6# Ze wzorow trygonometrycznych poszukiwany kat mozna z arcustangensa
        radiany = -atan2(sinus, cosinus)

        # 7# Zwroc poszukiwany kat w radianach i stopniach
        kat_dwuscienny = {"rad": radiany, "deg": rad2deg(radiany)}

    except ValueError as err:
        kat_dwuscienny = {"rad": err, "deg": err}

    return kat_dwuscienny

