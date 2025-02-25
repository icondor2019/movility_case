# Cost of Living Prediction in H8 Hexagons  

## Project Overview  
This project focuses on predicting the **cost of living** in H8 hexagons using mobility-related data and additional geographical context. The dataset was stored in **Parquet format** and was processed in batches using **Dask** to handle its large size efficiently.  

The approach involved:  
- **Data Processing**: Handling a large Parquet dataset with Dask in a batch-wise manner.  
- **Missing Data Imputation**: Using **KNN Imputer** to fill in missing values.  
- **Feature Engineering**: Enriching the dataset with external information about important geographical points such as **malls, banks, universities, and schools**.  
- **Modeling**: Building a **Random Forest Regression** model using **Scikit-Learn**.  
- **Geographical Data Handling**: Managing and processing spatial data to incorporate relevant mobility-related features.  

---

## Data Processing  
### 1. **Handling a Large Parquet File with Dask**  
- Due to the dataset's size, Dask was used for **parallel processing** and **batch handling**.  
- Dask's dataframe API was leveraged to perform **efficient filtering, transformations, and aggregations**.  

### 2. **Dealing with Missing Values**  
- A **KNN Imputer** was used to estimate missing values based on the nearest neighbors in the dataset.  

### 3. **Enriching Data with External Sources**  
- Additional geographical data was integrated, covering key **points of interest (POIs)** such as:  
  - Shopping malls  
  - Banks  
  - Universities  
  - Schools  
- This external data helped enhance model features by incorporating proximity-based insights.  

---

## Model Training  
- The target variable was the **cost of living in an H8 hexagon**.  
- A **Random Forest Regressor** was chosen for its robustness in handling nonlinear relationships and feature interactions.  
- The dataset included a mix of **mobility data and geographical features**, allowing the model to capture complex spatial patterns.  

### **Modeling Steps**  
1. Data preprocessing (normalization, encoding categorical variables).  
2. Feature selection and engineering based on geographical attributes.  
3. Training and evaluation using **cross-validation**.  
4. Model tuning and performance optimization.  

---

## Challenges & Solutions  
### **1. Large Dataset Management**  
- **Solution:** Used **Dask** to process data in batches instead of loading everything into memory.  

### **2. Missing Data Handling**  
- **Solution:** Implemented **KNN Imputer** to infer missing values instead of dropping incomplete rows.  

### **3. Integrating External Geographical Data**  
- **Solution:** Merged spatial information with the main dataset using **geospatial joins** and calculated distances to relevant POIs.  

---

## Results & Insights  
- The model successfully captured mobility-driven cost-of-living variations across H8 hexagons.  
- The addition of geographical POIs improved predictive performance by adding **location-based context**.  
- The approach demonstrated the power of **batch processing with Dask** and **geospatial data fusion** in real-world cost-of-living predictions.  

---

## Tools & Technologies  
- **Dask** (for big data processing)  
- **Scikit-Learn** (for machine learning)  
- **Pandas & Geopandas** (for data manipulation)  
- **Parquet** (for optimized storage and retrieval)  
- **KNN Imputer** (for handling missing values)  

---

## Future Improvements  
- **Experimenting with Deep Learning**: Using neural networks for feature extraction.  
- **Adding More Geospatial Features**: Incorporating additional POI types like hospitals, parks, and public transport stations.  
- **Refining Mobility Data Usage**: Exploring alternative mobility datasets for improved predictions.  

