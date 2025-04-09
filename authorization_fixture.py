@pytest.fixture(scope="session")
 async def authenticated_ac(register_user, ac):
     await ac.post(
         "/auth/login",
         json={
             "email": "kot@pes.com",
             "password": "1234"
         }
     )
     assert ac.cookies["access_token"]
     yield ac