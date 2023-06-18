# EVChargeMap
A Streamlit-based application to visualizes Electric Vehicle charging stations across France using a data set from data.gouv.fr, demonstrating how easy it is to deploy such web pages on Clever Cloud

## To deploy on Clever Cloud

Just clone/fork this repository and use the code as-is. Then add this environnement variable to your application :

```
CC_RUN_COMMAND = streamlit run src/app.py
```
Thus, the application will start with this command, listening to port 9000 (as configured in `.streamlit/config.toml`).
