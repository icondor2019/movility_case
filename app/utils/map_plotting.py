import folium
import h3
import geopandas as gpd
# from shapely.geometry import Point
# from shapely.ops import unary_union
from shapely.geometry import Polygon


def hex_to_polygon(hex_id):
    boundary = h3.cell_to_boundary(hex_id)
    return Polygon(boundary), boundary


def plot_hex_map(df_train, hue_variable=None, hex_colum='hex', color_map={1: "red", 0: "green"}):

    # extract coordinates from hexagons
    df_train['geometry'], df_train['coordinates'] = zip(*df_train[hex_colum].apply(hex_to_polygon))

    # Convert DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df_train, geometry='geometry')

    # Get center for the map (average lat/lon of hexagons)
    centroid = gdf.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=3, tiles="cartodbpositron")

    # Add hexagons to the map
    if hue_variable:
        len_color = df_train[hue_variable].nunique()
        if len_color > len(color_map):
            return 'mas variables que colores...'
        for _, row in gdf.iterrows():
            folium.Polygon(
                locations=row['coordinates'],
                color=color_map[row[hue_variable]],
                fill=True,
                fill_color=color_map[row[hue_variable]],
                fill_opacity=0.5,
                tooltip=row[hex_colum],
            ).add_to(m)
    else:
        for _, row in gdf.iterrows():
            folium.Polygon(
                locations=row['coordinates'],
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.5,
                tooltip=row[hex_colum],
            ).add_to(m)
    return m


def plot_hex_n_points(gdf_points):
    # Crear el mapa centrado en el primer punto
    centroid = gdf_points.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles="cartodbpositron")

    # Colores para los puntos importantes
    point_color = 'red'
    # hex_color = 'yellow'

    # Dibujar los puntos en el mapa
    for _, row in gdf_points.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=6,
            color=point_color,
            fill=True,
            fill_color=point_color
        ).add_to(m)

    # Dibujar los hexágonos H8 correspondientes a cada punto
    for _, row in gdf_points.iterrows():
        # Obtener las coordenadas de los límites del hexágono
        hex_boundary = h3.cell_to_boundary(row['hex_id'])
        color_map = {1: "green", 2: "yellow", 0: "blue"}
        # Dibujar el hexágono en el mapa
        folium.Polygon(
            locations=hex_boundary,
            color=color_map[row['cost_of_living']],
            fill=True,
            fill_color=color_map[row['cost_of_living']],
            fill_opacity=0.3
        ).add_to(m)

    return m
