import consul

def show_scraping_type(domain,hst):
  C = consul.Consul(host=f'10.10.{hst}')
  key=f'data-factory/production/services/scraping_service/domain_config/{domain}/scraping_type'
  kv = C.kv.get(key=key)
  try:
    scrap_type = kv[1].get('Value').decode('utf-8')
    return print (f"Scraping type for this site is => {scrap_type}")
  except:
    return print("No assigned scraping type for this site! So, by default, it's 'Oxylabs Universal'")