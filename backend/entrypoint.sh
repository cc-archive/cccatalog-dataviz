cd scripts
echo "Starting Build Script"
python ./build_adj_list_db.py
echo "dB Successfully Built"
echo "Copying the dB into ../src/dataviz_api/data"
cp * ../src/dataviz_api/data
echo "Copy Success"
cd ../src

echo "Making Migrations"
python manage.py makemigrations
echo "Migrations Complete"
echo "Migrating..."
python manage.py migrate
echo "Migrate Success"

echo "Adding Nodes Metadata Into SQL Lite dB"
python ./manage.py shell < ./add_nodes_to_db.py
echo "Nodes Metadata Added Successfully"