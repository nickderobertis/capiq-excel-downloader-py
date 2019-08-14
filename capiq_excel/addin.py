from exceldriver.addin import load_addin

def load_capiq(excel):
    return load_addin(excel, 'S&P Capital IQ Excel Plug-in')


