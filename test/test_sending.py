# def test_send_mail(authorized_client):
#     response = authorized_client.post('/send/one',
#                                       data={
#                                                   "email": "prusik.kacper1@gmail.com",
#                                                   "name": "Kacper Prusik",
#                                                   "subject": "Oferta praktyk",
#                                                   "content": "Cześć, szukam praktyk!"
#                                               })
#
#
#
#     assert response.status_code == 200, response.text


def test_send_mail(authorized_client):
    response = authorized_client.post('/send/one',
                                          data={
                                              "email": "prusik.kacper1@gmail.com",
                                              "name": "Kacper Prusik",
                                              "subject": "Oferta praktyk",
                                              "content": "Cześć, szukam praktyk!"
                                          })

    assert response.status_code == 200, response.text