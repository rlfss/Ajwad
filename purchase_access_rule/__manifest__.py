{
	'name': "Purchase Access Rule",
	'summary': "Access rule for purchase order and RFQ",
	'auther': "Muram Makkawi",
        'version': "0.1.1",
	'category':'Purchase',
	'depends': ['purchase'],
	'data': [
		'security/purchase_security.xml',
		'security/ir.model.access.csv',
		],		
	'installable': True,
	'license': 'OEEL-1',

}
