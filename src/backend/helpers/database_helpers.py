import logging 
LOGGER = logging.getLogger(__name__)

def build_dynamic_update_query_template(dataColumns: dict, keyName: str):
    setAttributesList = []
    for columnName, options in dataColumns.items():
        if columnName != keyName:
            setAttributesList.append( \
                f'{columnName} = %({columnName})s' if options.get('setToNullOnNonUpdate') \
                else f'{columnName} = COALESCE(%({columnName})s, {columnName})'
            )
    setAttributeValues = '\t' + ',\n\t'.join(setAttributesList)
    return f"""
    UPDATE {{tableName}}
    SET
    {setAttributeValues}
    WHERE {{keyName}} = %({{keyName}})s
    RETURNING *
    """
