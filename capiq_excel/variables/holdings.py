from dataconfig.variables import variable_display_names as vd

from .tools import _date_strs_from_date_range


start_date = '12/31/2007'
end_date = '12/31/2017'
freq = 'Q'

date_strs = _date_strs_from_date_range(start_date, end_date, freq)

institutional_variables = {
    'IQ_INSTITUTIONAL_NAME': vd.holding_institution,
    'IQ_INSTITUTIONAL_CIQID': vd.institution_cqid,
    'IQ_INSTITUTIONAL_SHARES': vd.institutional_shares
}

insider_variables = {
    'IQ_INSIDER_NAME': vd.insider_name,
    'IQ_INSIDER_CIQID': vd.insider_cqid,
    'IQ_INSIDER_SHARES': vd.insider_shares
}


