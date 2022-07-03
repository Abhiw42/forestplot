import pandas.api.types as ptypes
import pandas as pd
from typing import Optional, List, Union, Tuple
import warnings


def check_data(
    dataframe: pd.core.frame.DataFrame,
    estimate: str,
    varlabel: str,
    moerror: Optional[str] = None,
    ll: Optional[str] = None,
    hl: Optional[str] = None,
    addannote: Optional[Union[list, tuple]] = None,
    annoteheaders: Optional[Union[list, tuple]] = None,
    rightannote: Optional[Union[list, tuple]] = None,
    right_annoteheaders: Optional[Union[list, tuple]] = None,
) -> pd.core.frame.DataFrame:
    """
	Checks and validate that dataframe has the correct data. If data is missing, create them.
	Checks and validates key arguments.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	estimate (str)
		Name of column containing the estimates (e.g. pearson correlation coefficient,
		OR, regression estimates, etc.).
	moerror (str)
		Name of column containing the margin of error in the confidence intervals.
		Should be available if 'll' and 'hl' are left empty.
	ll (str)
		Name of column containing the lower limit of the confidence intervals. 
		Optional
	hl (str)
		Name of column containing the upper limit of the confidence intervals. 
	addannote (list-like)
		List of columns to add as additional annotation in the plot.
	annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations.
	
	Returns
	-------
		pd.core.frame.DataFrame.	
	"""
    ##########################################################################
    ## Check that numeric data are numeric
    ##########################################################################
    if not isinstance(dataframe, pd.core.frame.DataFrame):
        raise TypeError("Expect data as Pandas DataFrame")

    if not ptypes.is_numeric_dtype(dataframe[estimate]):
        try:
            dataframe[estimate] = dataframe[estimate].astype(float)
        except ValueError:
            raise TypeError("Estimates should be float or int")

    if moerror is not None:
        if not ptypes.is_numeric_dtype(dataframe[moerror]):
            try:
                dataframe[moerror] = dataframe[moerror].astype(float)
            except ValueError:
                raise TypeError("Margin of error values should be float or int")

    if ll is not None:
        if not ptypes.is_numeric_dtype(dataframe[ll]):
            try:
                dataframe[ll] = dataframe[ll].astype(float)
            except ValueError:
                raise TypeError("CI lowerlimit values should be float or int")

    if hl is not None:
        if not ptypes.is_numeric_dtype(dataframe[hl]):
            try:
                dataframe[hl] = dataframe[hl].astype(float)
            except ValueError:
                raise TypeError("CI higherlimit values should be float or int")

    ##########################################################################
    ## Check that either moerror or ll, hl are specified.
    ## Create the missing data from what is available
    ##########################################################################
    if moerror is None:
        try:
            assert (ll is not None) & (hl is not None)
        except:
            raise AssertionError(
                'If "moerror" is not provided, then "ll" and "hl" must be provided.'
            )

    if (ll is None) or (hl is None):
        try:
            assert moerror is not None
        except:
            raise AssertionError(
                'If "ll, hl" is not provided, then "moerror" must be provided.'
            )

    # if moerror not there make it
    if moerror is None:
        dataframe["moerror"] = dataframe[estimate] - dataframe[ll]

    # if ll, hl not there make it
    if ll is None:
        dataframe["ll"] = dataframe[estimate] - dataframe[moerror]
    if hl is None:
        dataframe["hl"] = dataframe[estimate] + dataframe[moerror]

    ##########################################################################
    ## Check that the annotations and headers specified are list-like
    ##########################################################################
    if addannote is not None:
        try:
            assert ptypes.is_list_like(addannote)
        except:
            raise TypeError("addannote should be list-like.")

    if annoteheaders is not None:
        try:
            assert ptypes.is_list_like(annoteheaders)
        except:
            raise TypeError("annoteheaders should be list-like.")

    if rightannote is not None:
        try:
            assert ptypes.is_list_like(rightannote)
        except:
            raise TypeError("rightannote should be list-like.")

    if right_annoteheaders is not None:
        try:
            assert ptypes.is_list_like(right_annoteheaders)
        except:
            raise TypeError("right_annoteheaders should be list-like.")

    ##########################################################################
    ## Check that annotations and corresponding headers have same length
    ##########################################################################
    # Check addannote and annoteheader same len
    if (addannote is not None) & (annoteheaders is not None):
        try:
            assert len(addannote) == len(annoteheaders)
        except:
            raise AssertionError("addannote and annoteheaders should have same length.")

    # Check rightannote and right_annoteheaders same len
    if (rightannote is not None) & (right_annoteheaders is not None):
        try:
            assert len(rightannote) == len(right_annoteheaders)
        except:
            raise AssertionError(
                "rightannote and right_annoteheaders should have same length."
            )

    ##########################################################################
    ## Check that specified annotations can be found in input or processed dataframe
    ##########################################################################
    acceptable_annotations = [ # from processed data
        "ci_range",
        "est_ci",
        "formatted_pval",
    ]  

    if addannote is not None:
        for col in addannote:
            try:
                assert (col in dataframe.columns) or (col in acceptable_annotations)
            except:
                raise AssertionError(f"the field {col} is not found in dataframe.")

    if rightannote is not None:
        for col in rightannote:
            try:
                assert (col in dataframe.columns) or (col in acceptable_annotations)
            except:
                raise AssertionError(f"the field {col} is not found in dataframe.")

    ##########################################################################
    ## Warnings
    ##########################################################################
    # Warn: Check that var itself is not in addannote
    if (addannote is not None) and (varlabel in addannote):
        warnings.warn(
            f'{varlabel} is a variable is already printed. Specifying {varlabel} in "addannote" will lead to duplicate printing of {varlabel}.'
        )

    if (rightannote is not None) and (varlabel in rightannote):
        warnings.warn(f"{varlabel} is a variable is already printed.")
        # warnings.warn(f'Specifying {varlabel} in "rightannote" will lead to duplicate printing of {varlabel}.')
        warnings.warn(
            f'{varlabel} is a variable is already printed. Specifying {varlabel} in "rightannote" will lead to duplicate printing of {varlabel}.'
        )

    # Warn: need to ignore ylabel if annoteheaders are specified
    # Warn: need to ignore ylabel2 if right_annote headers are specified

    # Warn: Need to ignore pval plotting if right_annote is specified

    # Warn duplicate labels in left and right side
    return dataframe
