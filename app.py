from contextlib import contextmanager
from io import StringIO
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
import streamlit as st
import sys
import re
import sng

import whois

def is_domain_available(domain):
    try:
        get_info = whois.whois(domain)
        return "Il dominio "+domain +" è già stato acquistato " 
    except:
        return "Il dominio "+domain +" è diponibile per essere acquistato "

@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b)
                output_func(buffer.getvalue())
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    with st_redirect(sys.stderr, dst):
        yield



def strToList(textArea):
	listaNomi = []
	for nomi in textArea:
		nomi = nomi.replace('\n', '')
		nomi = nomi.replace('.', '')
		nomi = re.sub('[^a-zA-Z.\d\s]', '', nomi.lower())
		as_list = nomi.split(" ")
		for sottoNomi in as_list :
			listaNomi.append(sottoNomi)
	return listaNomi

def stampaEControllaDominio(listNomiStartup):
	for nomeStartup in listNomiStartup:
		with st.expander(nomeStartup):
			nomeStartup = nomeStartup.replace(' ', '')
			st.write(is_domain_available(nomeStartup+".it") + "+  [Info](https://whois.domaintools.com/"+(nomeStartup+".it")+")")
			st.write(is_domain_available(nomeStartup+".com")+"+  [Info](https://whois.domaintools.com/"+(nomeStartup+".com")+")")
			st.write(is_domain_available(nomeStartup+".net") + "+  [Info](https://whois.domaintools.com/"+(nomeStartup+".net")+")")
			st.write(is_domain_available(nomeStartup+".org") + "+  [Info](https://whois.domaintools.com/"+(nomeStartup+".org")+")")
			st.write(is_domain_available(nomeStartup+".shop") + "+  [Info](https://whois.domaintools.com/"+(nomeStartup+".shop")+")")




def saluti():
	st.markdown('<bold> Se ti è stato di aiuto condividi il nostro sito per supportarci </bold>\
	   <ul> \
	  <li><a href="https://www.facebook.com/sharer.php?u=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F" target="blank" rel="noopener noreferrer">Condividi su Facebook</a></li> \
	  <li><a href="https://twitter.com/intent/tweet?url=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F&text=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale." target="blank" rel="noopener noreferrer">Condividi su Twitter</a></li> \
	  <li><a href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.intelligenzaartificialeitalia.net%2F&title=IntelligenzaArtificialeItalia=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale.&source=IntelligenzaArtificialeItalia" target="blank" rel="noopener noreferrer">Condividi su Linkedin</a></li>\
	</ul>', unsafe_allow_html=True)





st.set_page_config(page_title="Generatore di Nomi per Startup", page_icon="📚", layout='wide', initial_sidebar_state='auto')

st.markdown("<center><h1> Genera nomi per la Tua STARTUP con la nostra I.A. <small><br> Powered by INTELLIGENZAARTIFICIALEITALIA.NET </small></h1>", unsafe_allow_html=True)
st.write('<p style="text-align: center;font-size:15px;" > <bold>Stanco di doverti screvellare per trovare un nome alla tua startup con il dominio disponibile ? <bold>  </bold> Da oggi ti ispiriamo noi<p><br><bold>PS: I nomi generati sono unici quindi puoi anche rivenderteli se ti piacciono</bold>', unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.subheader("Genera nomi per Startup con la nostra rete Neurale !")


def main():
	activity1 = ["Usa modelli preconfigurati","Crea il tuo Modello personalizzato"]
	choice = st.selectbox("Seleziona come inserire il testo da tradurre",activity1)
	if choice == 'Usa modelli preconfigurati':
		col1, col2 = st.columns(2)		
		col3, col4 = st.columns(2)
		col5, col6 = st.columns(2)
		with col1:
			epochs = st.slider('Numero di epochs :', 20, 500,50,10)
		with col2:
			numero_nomi = st.slider('Quanti nomi vuoi generare :', 10, 50,15,5)	
		with col3:
			max_word_len = st.slider('Lunghezza massima del nome :', 5, 50,10,1)
		with col4:
			min_word_len = st.slider('Lunghezza minima del nome :', 3, 50,5,1)
		with col5:
			suffix = st.text_input('In che ambito opera la tua startup', ' Software')
		

		cfg = sng.Config(
		    epochs = epochs,
		    max_word_len = max_word_len,
		    min_word_len = min_word_len,
		    suffix = suffix
		)
		#st.write("Configurazione Salvata con successo ")
		#st.write(cfg.to_dict())
		with col6:
			ispirazioni = st.selectbox("Seleziona dove vuoi che prenda ispirazione la Rete Neurale",sng.show_builtin_wordlists(),index=6)
		if st.button("Genera i nomi") :
			with st.spinner('Aspetta mentre la rete si allena...'):
				with st_stdout("code"):
					gen = sng.Generator(wordlist=sng.load_builtin_wordlist(ispirazioni), config=cfg)
					gen.fit()
			nomiGenerati = gen.simulate(n=numero_nomi)
			stampaEControllaDominio(nomiGenerati)

			saluti()
		
		
	if choice == 'Crea il tuo Modello personalizzato':

		col1, col2 = st.columns(2)		
		col3, col4 = st.columns(2)
		col5, col6 = st.columns(2)
		col7, col8 = st.columns(2)
		with col1:
			epochs = st.slider('Numero di epochs :', 20, 500,50,10)
		with col2:
			numero_nomi = st.slider('Quanti nomi vuoi generare :', 10, 50,15,5)	
		with col3:
			max_word_len = st.slider('Lunghezza massima del nome :', 5, 50,10,1)
		with col4:
			min_word_len = st.slider('Lunghezza minima del nome :', 3, 50,5,1)
		with col5:
			batch_size = st.slider('Numero di batch_size :', 32, 1024,64)
		with col6:
			hidden_dim = st.slider('Numero di hidden_dim :', 20, 150,50,10)
		with col7:
			n_layers = st.slider('Numero di layer :', 1, 10,2,1)
		with col8:
			temperature = st.slider('Temperatura :', 0.1, 2.1,1.0,0.1)


		suffix = st.text_input('In che ambito opera la tua startup', ' Software')


		cfg = sng.Config(
		    epochs = epochs,
		    batch_size = batch_size,
		    hidden_dim = hidden_dim,
		    max_word_len = max_word_len,
		    min_word_len = min_word_len,
		    n_layers = n_layers,
		    temperature = temperature,
		    suffix = suffix
		)
		st.write("Configurazione Salvata con successo ")
		st.write(cfg.to_dict())

		inserimento = ["Manualmente","File .txt"]
		choice = st.selectbox("Seleziona come inserire il testo da cui prendere ispirazione. E' importante che ci sia una al massimo due parole per riga",inserimento)
		if choice == 'Manualmente':
			txt = st.text_area('Inserisci delle parole o nomi', '''
			Amazon
			Google
			Facebook
			Netflix
			TikTok
			New Balance
			Sky
			Mediaset
			Nike
			Adidas
			Just Eat
			''',height=350)
			if st.button("Genera i nomi") :
				nomiGen= strToList(txt)
				with st.spinner('Aspetta mentre la rete si allena...'):
					with st_stdout("code"):
						gen = sng.Generator(wordlist=nomiGen, config=cfg)
						gen.fit()
				nomiGenerati = gen.simulate(n=numero_nomi)
				stampaEControllaDominio(nomiGenerati)

				saluti()
		
		if choice == 'File .txt':
			uploaded_file = st.file_uploader("Carica il file txt", type="txt", accept_multiple_files=False)
			with st.expander("Scarica un file d'esempio"):
				with open('startupName.txt', 'rb') as f:
	  				st.download_button("Scarica un file .txt contenente più di 100 nomi di famose aziende", f, file_name='startupName.txt') 
			if uploaded_file:
				if st.button("Genera i nomi") :
					l = []
					for line in uploaded_file:
						l.append(str(line)+"\n")
					nomiGen= strToList(l)
					with st.spinner('Aspetta mentre la rete si allena...'):
						with st_stdout("code"):
							gen = sng.Generator(wordlist=nomiGen, config=cfg)
							gen.fit()
					nomiGenerati = gen.simulate(n=numero_nomi)
					stampaEControllaDominio(nomiGenerati)

					saluti()			
	
	st.text("")
	st.text("")
	st.text("")
	st.text("")
	st.text("")
	st.text("")
	st.text("")
	st.write("Proprietà intellettuale di [Intelligenza Artificiale Italia © ](https://intelligenzaartificialeitalia.net)")
	st.write("Hai un idea e vuoi realizzare un Applicazione Web Intelligente? contatta il nostro [Team di sviluppatori © ](mailto:python.ai.solution@gmail.com)")

if __name__ == '__main__':
	main()
