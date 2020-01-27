ADS_QUERY = """
SELECT ('{ "annonsId": '||(doc::jsonb->'annonsId')::text||', 
           "uppdateradTid": '||(doc::jsonb->'uppdateradTid')::text||', 
           "avpublicerad": '||(doc::jsonb->'avpublicerad')::text||'
           }')::jsonb
FROM platsannons_la
WHERE id in %s;
"""

AD_ANNONSTEXT_QUERY = """
SELECT doc::json-> 'annonstext', doc::json-> 'annonstextFormaterad'
FROM platsannons_la pl
WHERE id = %s;
"""

AD_ALL_QUERY = """
SELECT doc::jsonb -'annonstext' -'annonstextFormaterad'
FROM platsannons_la pl
WHERE id = %s;
"""