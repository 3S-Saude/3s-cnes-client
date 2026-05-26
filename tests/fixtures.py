"""Fixtures SOAP usadas pela suíte sem acessar o serviço real."""

SOAP_SUCCESS_RESPONSE = b"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body>
    <cnes:responseConsultarEstabelecimentoSaude
      xmlns:cnes="http://servicos.saude.gov.br/cnes/v1r0/cnesservice">
      <res:ResultadoPesquisaEstabelecimentoSaude
        xmlns:res="http://servicos.saude.gov.br/wsdl/mensageria/v1r0/resultadopesquisaestabelecimentosaude">
        <res:EstabelecimentoSaude>
          <cod:CodigoCNES xmlns:cod="http://servicos.saude.gov.br/schema/cnes/v1r0/codigocnes">
            <cod:codigo>2400737</cod:codigo>
          </cod:CodigoCNES>
          <un:CodigoUnidade xmlns:un="http://servicos.saude.gov.br/schema/cnes/v1r0/codigounidade">
            <un:codigo>0001</un:codigo>
          </un:CodigoUnidade>
          <est:nomeFantasia xmlns:est="http://servicos.saude.gov.br/schema/cnes/v1r0/dadosgeraiscnes">
            <nome:Nome xmlns:nome="http://servicos.saude.gov.br/schema/corporativo/pessoajuridica/v1r0/nomejuridico">Hospital Exemplo</nome:Nome>
          </est:nomeFantasia>
          <est:nomeEmpresarial xmlns:est="http://servicos.saude.gov.br/schema/cnes/v1r0/dadosgeraiscnes">
            <nome:Nome xmlns:nome="http://servicos.saude.gov.br/schema/corporativo/pessoajuridica/v1r0/nomejuridico">Hospital Exemplo LTDA</nome:Nome>
          </est:nomeEmpresarial>
          <cnpj:CNPJ xmlns:cnpj="http://servicos.saude.gov.br/schema/corporativo/pessoajuridica/v1r0/cnpj">
            <cnpj:numeroCNPJ>00000000000000</cnpj:numeroCNPJ>
          </cnpj:CNPJ>
          <end:Endereco xmlns:end="http://servicos.saude.gov.br/schema/corporativo/endereco/v1r2/endereco">
            <end:TipoLogradouro>
              <tl:descricaoTipoLogradouro xmlns:tl="http://servicos.saude.gov.br/schema/corporativo/endereco/v1r1/tipologradouro">Rua</tl:descricaoTipoLogradouro>
            </end:TipoLogradouro>
            <end:nomeLogradouro>Exemplo</end:nomeLogradouro>
            <end:numero>100</end:numero>
            <end:complemento>Sala 1</end:complemento>
            <end:Bairro>
              <bairro:descricaoBairro xmlns:bairro="http://servicos.saude.gov.br/schema/corporativo/endereco/v1r1/bairro">Centro</bairro:descricaoBairro>
            </end:Bairro>
            <end:CEP>
              <cep:numeroCEP xmlns:cep="http://servicos.saude.gov.br/schema/corporativo/endereco/v1r1/cep">59000000</cep:numeroCEP>
            </end:CEP>
            <end:Municipio>
              <mun:codigoMunicipio xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">240810</mun:codigoMunicipio>
              <mun:nomeMunicipio xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">Natal</mun:nomeMunicipio>
              <mun:UF xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">
                <uf:siglaUF xmlns:uf="http://servicos.saude.gov.br/schema/corporativo/v1r1/uf">RN</uf:siglaUF>
              </mun:UF>
            </end:Municipio>
          </end:Endereco>
          <est:dataAtualizacao xmlns:est="http://servicos.saude.gov.br/schema/cnes/v1r0/dadosgeraiscnes">2026-05-26</est:dataAtualizacao>
          <tu:tipoUnidade xmlns:tu="http://servicos.saude.gov.br/schema/cnes/v1r0/tipounidade">
            <tu:codigo>05</tu:codigo>
            <tu:descricao>Hospital Geral</tu:descricao>
          </tu:tipoUnidade>
          <ea:esferaAdministrativa xmlns:ea="http://servicos.saude.gov.br/schema/cnes/v1r0/esferaadministrativa">
            <ea:codigo>04</ea:codigo>
            <ea:descricao>Municipal</ea:descricao>
          </ea:esferaAdministrativa>
          <est:MunicipioGestor xmlns:est="http://servicos.saude.gov.br/schema/cnes/v1r0/dadosgeraiscnes">
            <mun:codigoMunicipio xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">240810</mun:codigoMunicipio>
            <mun:nomeMunicipio xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">Natal</mun:nomeMunicipio>
            <mun:UF xmlns:mun="http://servicos.saude.gov.br/schema/corporativo/v1r2/municipio">
              <uf:siglaUF xmlns:uf="http://servicos.saude.gov.br/schema/corporativo/v1r1/uf">RN</uf:siglaUF>
            </mun:UF>
          </est:MunicipioGestor>
          <tel:Telefone xmlns:tel="http://servicos.saude.gov.br/schema/corporativo/telefone/v1r2/telefone">
            <tel:DDI>55</tel:DDI>
            <tel:DDD>84</tel:DDD>
            <tel:numeroTelefone>40000000</tel:numeroTelefone>
          </tel:Telefone>
          <email:Email xmlns:email="http://servicos.saude.gov.br/schema/corporativo/v1r2/email">
            <email:descricaoEmail>contato@example.org</email:descricaoEmail>
            <email:tipoEmail>A</email:tipoEmail>
          </email:Email>
          <loc:Localizacao xmlns:loc="http://servicos.saude.gov.br/schema/cnes/v1r0/localizacao">
            <loc:longitude>-35.2</loc:longitude>
            <loc:latitude>-5.8</loc:latitude>
          </loc:Localizacao>
          <est:perteceSistemaSUS xmlns:est="http://servicos.saude.gov.br/schema/cnes/v1r0/dadosgeraiscnes">true</est:perteceSistemaSUS>
        </res:EstabelecimentoSaude>
        <res:sumario>
          <res:quantidadeProfissionaisSaude>1</res:quantidadeProfissionaisSaude>
          <res:quantidadeCBOS>2</res:quantidadeCBOS>
          <res:quantidadeLeitos>3</res:quantidadeLeitos>
          <res:quantidadeHabilitacoes>4</res:quantidadeHabilitacoes>
          <res:quantidadeEquipamentos>5</res:quantidadeEquipamentos>
          <res:quantidadeSamus>0</res:quantidadeSamus>
        </res:sumario>
      </res:ResultadoPesquisaEstabelecimentoSaude>
    </cnes:responseConsultarEstabelecimentoSaude>
  </soap:Body>
</soap:Envelope>
"""

SOAP_EMPTY_RESPONSE = b"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body>
    <cnes:responseConsultarEstabelecimentoSaude
      xmlns:cnes="http://servicos.saude.gov.br/cnes/v1r0/cnesservice">
      <res:ResultadoPesquisaEstabelecimentoSaude
        xmlns:res="http://servicos.saude.gov.br/wsdl/mensageria/v1r0/resultadopesquisaestabelecimentosaude">
        <res:sumario>
          <res:quantidadeProfissionaisSaude>0</res:quantidadeProfissionaisSaude>
          <res:quantidadeCBOS>0</res:quantidadeCBOS>
          <res:quantidadeLeitos>0</res:quantidadeLeitos>
          <res:quantidadeHabilitacoes>0</res:quantidadeHabilitacoes>
          <res:quantidadeEquipamentos>0</res:quantidadeEquipamentos>
          <res:quantidadeSamus>0</res:quantidadeSamus>
        </res:sumario>
      </res:ResultadoPesquisaEstabelecimentoSaude>
    </cnes:responseConsultarEstabelecimentoSaude>
  </soap:Body>
</soap:Envelope>
"""

SOAP_FAULT_RESPONSE = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body>
    <soap:Fault>
      <soap:Code>
        <soap:Value>soap:Sender</soap:Value>
      </soap:Code>
      <soap:Reason>
        <soap:Text>Falha na consulta do CNES.</soap:Text>
      </soap:Reason>
      <soap:Detail>
        <ms:MSFalha xmlns:ms="http://servicos.saude.gov.br/wsdl/mensageria/falha/v5r0/msfalha">
          <ms:identificador>abc-123</ms:identificador>
          <ms:Mensagem>
            <msg:codigo xmlns:msg="http://servicos.saude.gov.br/wsdl/mensageria/falha/v5r0/mensagem">CNES-001</msg:codigo>
            <msg:descricao xmlns:msg="http://servicos.saude.gov.br/wsdl/mensageria/falha/v5r0/mensagem">CNES inválido.</msg:descricao>
          </ms:Mensagem>
        </ms:MSFalha>
      </soap:Detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
""".encode()
