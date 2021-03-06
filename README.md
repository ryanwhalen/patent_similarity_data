# Patent Similarity Data and Measures
US utility patent similarity data creation and analysis tools. 

The Jupyter notebook (patent_sim_data_notebook.ipynb) demonstrates various uses for the dataset. **Start here** for an overview and introduction: https://github.com/ryanwhalen/patent_similarity_data/blob/master/patent_sim_data_notebook.ipynb

patent_d2v.py provides replication code for the Doc2Vec model computation, and vector extraction. 

write_sim_data_to_db.py provides code that will update a local version of a patent database with tables containing the patent similarity data shared at Zenodo: https://zenodo.org/record/3552078

Patent metadata and text to join to similarity data can be downloaded directly from the USPTO here:https://www.patentsview.org/download/. 
Alternately the script here will automate the downloading & database-making processes: https://github.com/ryanwhalen/patentsview_data_download

To reference this work, please cite: Whalen, R., Lungeanu, A., DeChurch, L. A., & Contractor, N. (2020). "Patent Similarity Data and Innovation Metrics." *Journal of Empirical Legal Studies.*

