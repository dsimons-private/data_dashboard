import pandas as pd
import plotly.graph_objs as go


def cleandata(dataset, keepcolumns, value_variables, countries):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file
        keepcolumns (list): define which columns shall be kept
        value_variables (list): define variables to be analysed
        countries(list): define list, which shall be analysed

    Returns:
        df_melt (pandas.DataFrame): wrangled dataframe

    """
    df = pd.read_csv(dataset, skiprows=4)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    df = df[df['Country Name'].isin(countries)]

    # melt year columns and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars=value_variables)
    df_melt.columns = ['country', 'year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # print(df_melt) # debug only

    # output clean csv file
    return df_melt


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # ***
    # first chart plots Current health expenditure per capita (current US$) in top 10 economies
    # as a line chart
    # ***

    graph_one = []
    df = cleandata('data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_2397.csv',
                   keepcolumns=['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   value_variables=['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   countries=['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France',
                              'Brazil', 'Italy', 'Canada']
                   )
    df.columns = ['country', 'year', 'variable']
    df.sort_values('year', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()

    for country in countrylist:
        x_val = df[df['country'] == country].year.tolist()
        y_val = df[df['country'] == country].variable.tolist()
        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_one = dict(title='Current health expenditure per capita (current US$)',
                      xaxis=dict(title='Year',
                                 autotick=False,
                                 tick0=2015,
                                 dtick=1),
                      yaxis=dict(title='US-Dollar($)'),
                      )
    # ***
    # second chart plots Current health expenditure per capita (current US$) in Germany as a bar chart
    # ***

    graph_two = []
    df = cleandata('data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_2397.csv',
                   keepcolumns=['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   value_variables=['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   countries=['Germany']
                   )

    df.columns = ['country', 'year', 'variable']
    df.sort_values('year', ascending=False, inplace=True)

    graph_two.append(
        go.Bar(
            x=df.year.tolist(),
            y=df.variable.tolist()
        )
    )

    layout_two = dict(title='GERMANY - Current health expenditure per capita (current US$)',
                      xaxis=dict(title='Year'),
                      yaxis=dict(title='US-Dollar($)')
                      )
    # ***
    # third chart plots DACH region in comparison
    # ***

    graph_three = []

    df = cleandata('data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_2397.csv',
                   keepcolumns=['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   value_variables=['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                   countries=['Germany', 'Austria', 'Switzerland']
                   )

    df.columns = ['country', 'year', 'variable']
    df.sort_values('year', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()

    for country in countrylist:
        x_val = df[df['country'] == country].year.tolist()
        y_val = df[df['country'] == country].variable.tolist()
        graph_three.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_three = dict(title='DACH Region - health expenditure comparison',
                        xaxis=dict(title='Year'),
                        yaxis=dict(title='US-Dollar($)'),
                        )

    # ***
    # fourth chart shows population above age 65 in percent for DACH region
    # ***

    graph_four = []

    df_2 = cleandata(
        dataset=r'data/API_SP.POP.65UP.TO.ZS_DS2_en_csv_v2_2339.csv',
        keepcolumns=['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
        value_variables=['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
        countries=['Germany', 'Austria', 'Switzerland'])

    df_2.columns = ['country', 'year', 'variable']
    df_2.sort_values('year', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()

    for country in countrylist:
        x_val = df_2[df_2['country'] == country].year.tolist()
        y_val = df_2[df_2['country'] == country].variable.tolist()
        graph_four.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='markers',
                name=country
            )
        )

    layout_four = dict(title='DACH Region - population above age 65 (%)',
                       xaxis=dict(title='Year'),
                       yaxis=dict(title='%'),
                       )

    # ***
    # append all charts to the figures list
    # ***

    figures = [dict(data=graph_one, layout=layout_one),
               dict(data=graph_two, layout=layout_two),
               dict(data=graph_three, layout=layout_three),
               dict(data=graph_four, layout=layout_four)]

    return figures


if __name__ == '__main__':
    cleandata(
        dataset=r'\data\API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_2397.csv',
        keepcolumns=['Country Name', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
        value_variables=['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
        countries=['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil',
                   'Italy', 'Canada'])
