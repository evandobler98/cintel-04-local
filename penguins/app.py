import plotly.express as px
import palmerpenguins
import seaborn as sns
from shiny import render 
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly

# Load Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
penguins = load_penguins()

ui.page_opts(title="Evan's Penguin Data", fillable=True)

with ui.layout_columns(): 
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def penguins_dt():
            return render.DataTable(filtered_data())  # Changed to filtered_data()

    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def penguins_dg():
            return render.DataGrid(filtered_data())  # Changed to filtered_data()

with ui.layout_columns(): 
    with ui.card(fill=True):
        ui.card_header("Plotly Histogram")

        @render_widget
        def plot1():
            scatterplot = px.histogram(
                data_frame=filtered_data(),  # Changed to filtered_data()
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
            ).update_layout(
                title={"text": "Palmer Penguins", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.selected_attribute(),
            )
            return scatterplot

    with ui.card():
        ui.card_header("Seaborn Histogram")

        @render.plot
        def plot2():
            ax = sns.histplot(
                data=filtered_data(),  # Changed to filtered_data()
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax

# Add a sidebar
with ui.sidebar(position="left", bg="#f8f8f8", open="open"):
    ui.h2("Sidebar")
    
    # Drop-Down menu
    ui.input_selectize(
        id="selected_attribute",
        label="Selected Attribute",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    
    # Numeric Input field
    ui.input_numeric(id="plotly_bin_count", label="Bin Count (Plotly)", value=10)
    
    # Slider input
    ui.input_slider(
        id="seaborn_bin_count", label="Bin Count (Seaborn)", min=3, max=21, value=7
    )

    # Checkbox filter
    ui.input_checkbox_group(
        id="selected_species_list",
        label="Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    
    # Insert dividing line
    ui.hr()
    
    # Insert link
    ui.a(
        "Source code on GitHub",
        href="https://github.com/evandobler98/cintel-02-data",
        target="_blank",
    )

# Insert a Plotly Scatterplot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            data_frame=filtered_data(),  # Changed to filtered_data()
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            symbol="island",
            labels={
                "bill_depth_mm": "Bill Depth",
                "bill_length_mm": "Bill Length",
                "species": "Species",
                "island": "Island"
            },
        )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    
    # Get the selected species from the checkbox input
    selected_species = input.selected_species_list()
    
    # Filter the dataset based on selected species
    filtered_df = penguins_df[penguins_df['species'].isin(selected_species)]
    
    return filtered_df