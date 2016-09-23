#format_restructured_to_numpy_doc

A script to convert restructured text comments of the generic form:

    :param param_name: description
    :return return_name: description

to
numpy doc string [format](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt):

    Parameters
    ----------
    param_name - type
        description
    Returns
    -------
    type
        description

This does not handle anything other than param / return, but does a good job of grabbing comments of form
"""doc started here
more description
:param:
or 
"""single line doc"""
And is smart about finding """, e.g., comments with quotes are on their own line, 
    and not to be around just any str

The script will retain all other code and comments.

A few options are provided within the script under the __main__ at bottom.