from app import app
from flask import render_template, request
from app.models import formopener
from app.models.model import AirbnbData
from io import StringIO

@app.route('/')
@app.route('/index')
def index():
    airbnb = AirbnbData()
    
    percs_per_borough = airbnb.percentiles_per_borough()
    obj_1 = [percs_per_borough.to_html(classes='data', header="true")] 
    
    top_ten_names = airbnb.popular_first_names()
    obj_3 = [top_ten_names.to_html(classes='data', header="true")] 
    
    plot_url = airbnb.price_range_hist()
    
    neighbourhood = request.args.get('neighbourhood', default='Williamsburg', type=str)
    mapData = airbnb.get_map_data(neighbourhood=neighbourhood).to_json(orient='records')
    
    neighbourhood_options = airbnb.get_neighbourhood_options()
    
    return render_template('index.html', 
                            obj_1=obj_1, 
                            obj_3=obj_3,
                            plot_url=plot_url,
                            mapData=mapData,
                            neighbourhood_options=neighbourhood_options,
                            currentSelection=neighbourhood)
