switch_links = {'Core224' : ['Fanout225', 'Trans218','PoE226', 'Link202', 'Link203', 'Link204', 'Link205',
                         'Fanout225', 'Matai310', 'DTS311','PLink219', 'Exta207', 'Juno216', 'Dploy228', 'Trans218' ],
        'Trans218' : ['LARCC301'],
        'LARCC301' : ['Juno302', 'Juno303'],
        'Juno216' : ['Juno304'],
        'Juno304' : ['Cisco305'],
        'DTS311' : ['DDMZ312'],
        'Matai310' : ['PDMZ321'],
        'Fanout225' : ['VoIP201'],
        'PLink219' : ['Atwo501'],
                        }

for swl, links in switch_links.iteritems():
        print (swl , links)
        for sw2 in links:
		print (swl, links, sw2)
