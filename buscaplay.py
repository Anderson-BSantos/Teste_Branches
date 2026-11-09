# from playwright.sync_api import sync_playwright
# from playwright.sync_api import TimeoutError
import pandas as pd
import re
import time

# Lista de cidades da Bahia (adicione mais!)
municipios = [
    "Salvador Bahia", "Feira de Santana", "Vitória da Conquista", 
    "Juazeiro Bahia", "Lauro de Freitas", "Camaçari", "Ilhéus",
    "Teixeira de Freitas", "Jequié Bahia", "Barreiras", "Alagoinhas",
    "Porto Seguro", "Simoes-Filho", "Paulo Afonso Bahia", "Eunápolis",
    "Santo Antônio de Jesus", "Valença", "Candeias", "Guanambi",
    "Jacobina", "Serrinha", "Senhor do Bonfim","Ibicaraí", "Irecê",
    "Itaberaba","Luís Eduardo Magalhães", "Campo Formoso", "Brumado",
    "Bom Jesus da Lapa",  "Itamaraju", "Morro do Chapéu","Itacaré",
    "Cruz das Almas", "Conceição do Coité", "Maragogipe", "Caetité",
    "São Francisco do Conde", "Conde", "Seabra", "Tucano","Itabuna",
    "Euclides da Cunha", "Ribeira do Pombal", "Mata de São João",
    "Caravelas Bahia","Pojuca", "Ituberá Bahia", "Amargosa Bahia",
    "Santa Maria da Vitória", "Remanso Bahia", "Uruçuca Bahia"
    
]

# Lista para armazenar os resultados
dados = []

def buscar_hoteis(playwright):
    browser = playwright.chromium.launch(headless=False)  # Modo invisível
    page = browser.new_page()

    
    for cidade in municipios:
        url = f"https://www.booking.com/searchresults.pt-br.html?ss={cidade}"+"bahia"
        page.goto(url)
        
        def fechar_anuncio(page):
            try:
                # Espera um curto período e tenta clicar no botão de fechar, se existir
                page.wait_for_selector('button[aria-label="Ignorar informações de login."]', timeout=3000)
                page.click('button[aria-label="Ignorar informações de login."]')
                print("Anúncio fechado com sucesso!")
            except:
                print("Nenhum anúncio encontrado, continuando...")

        fechar_anuncio(page) # <------------- Chama o verificador de Anuncio
        try:
            # Verifica se o elemento "Tenho flexibilidade" está visível
            if page.is_visible('span:has-text("Tenho flexibilidade")'):
                page.click('span:has-text("Tenho flexibilidade")')  # Clica na opção flexibilidade
            else:
                # Se o elemento não estiver visível, tenta o clique alternativo
                page.click('div [tabindex="-1"][class="a1139161bf"]')
                # Tenta novamente clicar na opção flexibilidade após a ação alternativa
                page.click('span:has-text("Tenho flexibilidade")')
        except TimeoutError:
            print("Erro de timeout ao tentar clicar no elemento")
            page.reload()  # Recarrega a página em caso de erro

       # --------------------------------------------------------------------------------------------------------- Seleciona uma semana - 5 dias no mês
        page.click('label:has-text("Uma semana")')
        
       # --------------------------------------------------------------------------------------------------------- Seleciona um mês 
        page.click('div [class="bb227126eb"]') #Fevereiro
        page.keyboard.press("Enter")
        #page.click('p:has-text("Não há acomodações que correspondam aos seus critérios de busca. Tente atualizar sua pesquisa.")') # <------- 
        time.sleep(1)
        
        # Esperar os preços carregarem
        page.wait_for_load_state('load')  # Espera a página carregar totalmente
        page.wait_for_selector('div[data-testid="property-card"]', timeout=30000)

        # Coletar informações
        hoteis = page.query_selector_all('div[data-testid="property-card"]')
        for hotel in hoteis[:5]:  # Pega apenas 3 por cidade
            nome = hotel.query_selector('div[data-testid="title"]').inner_text() if hotel.query_selector('div[data-testid="title"]') else "N/A"
            preco = hotel.query_selector('span[data-testid="price-and-discounted-price"]').inner_text() if hotel.query_selector('span[data-testid="price-and-discounted-price"]') else "N/A"
            text = hotel.query_selector('div[data-testid="review-score"]').inner_text() if hotel.query_selector('div[data-testid="review-score"]') else "N/A"
            nota = re.search(r'\d+,\d+', text).group(0) if re.search(r'\d+,\d+', text) else "5,0"
            print(cidade)
            #link = hotel.query_selector('a[data-testid="property-card-link"]').get_attribute("href") if hotel.query_selector('a[data-testid="property-card-link"]') else "N/A"
            """
            # --- Tratando o texto do preço-------------------------------
            # Remove "R$", espaços e converte para número corretamente
            preco_limpo = preco.replace("R$", "").replace(".", "").strip()
            preco_numerico = int(preco_limpo)  # Converte para inteiro
            # Divide por 5
            diaria = preco_numerico / 5
            """
            dados.append({"Cidade": cidade, "Hotel": nome, "Preço": preco, "Nota": nota})#, "Diária":diaria}) #, "Link": link})

    browser.close()

# Executar o Playwright
# with sync_playwright() as playwright:
    buscar_hoteis(playwright)

# Salvar os dados em CSV
df = pd.DataFrame(dados)
df.to_csv("hoteis_bahia1.csv", index=False, encoding="utf-8")
print("✅ Dados salvos em 'hoteis_bahia.csv'!")




# ------------------ANOTAÇÕES------------------------------------------------------------------------ ANOTAÇÕES--------------------

        #page.click('label[class="c624d7469d f034cf5568 a937b09340 a3214e5942 f8208e9f83"]')
                    # Usa o QuerySelector por Texto ----------- page.evaluate('document.querySelector("label:has-text(\'Uma semana\')").click()')
                    # page.evaluate('document.querySelector("label[for=\\":r6k:\\"]")')

# ------------------ANOTAÇÕES------------------------------------------------------------------------ ANOTAÇÕES--------------------