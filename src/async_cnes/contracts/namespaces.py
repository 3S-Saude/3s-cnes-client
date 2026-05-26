"""Namespaces do contrato SOAP oficial do CNES."""

SOAP12_NS = "http://www.w3.org/2003/05/soap-envelope"
SOAP11_NS = "http://schemas.xmlsoap.org/soap/envelope/"
CNES_SERVICE_NS = "http://servicos.saude.gov.br/cnes/v1r0/cnesservice"
CODIGO_CNES_NS = "http://servicos.saude.gov.br/schema/cnes/v1r0/codigocnes"
RESULTADO_ESTABELECIMENTO_NS = (
    "http://servicos.saude.gov.br/wsdl/mensageria/v1r0/resultadopesquisaestabelecimentosaude"
)

NSMAP = {
    "soap": SOAP12_NS,
    "cnes": CNES_SERVICE_NS,
    "cod": CODIGO_CNES_NS,
}
