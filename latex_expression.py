'''

a = "Selecione uma Região 🌏"
selected_region = st.radio(fr"$\large \textsf{{{a}}}$", 
                            options=regions,
                            index= 7
                            # format_func= lambda option: fr"$ \textsf{{{option}}}$"
                            )
                            
'''