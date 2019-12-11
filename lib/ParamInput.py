
def GetInitialParameters(fittype):
    initial_params = []
    if fittype in ["Gauss2","Gauss3"]:
        initial_params.append(input("First gaussian amplitude: "))
        initial_params.append(input("First gaussian mean: "))
        initial_params.append(input("First gaussian sigma: "))
        initial_params.append(input("Second gaussian amplitude: "))
        initial_params.append(input("Second gaussian mean: "))
        initial_params.append(input("Second gaussian sigma: "))
    if fittype == "Gauss3": 
        initial_params.append(input("third gaussian amplitude: "))
        initial_params.append(input("third gaussian mean: "))
        initial_params.append(input("third gaussian sigma: "))
    else:
        print("Fit type not recognized for inputting initial parameters!")
    return initial_params
