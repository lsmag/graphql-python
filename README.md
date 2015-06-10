    ast = graphql.parse("""
        User (234234) {
            one {
                sub1,
                sub2
            },
            two,
            three,
            four
        }
    """, flat=True|False)


flat=False by default, retorna um dict estilo https://github.com/madjam002/graphqlite
com a representação da query.

flat=True é diferente... provavelmente não terei. Veremos.


    {
      user(id: 3500401) {
        id,
        name,
        isViewerFriend,
        profilePicture(size: 50)  {
          uri,
          width,
          height
        }
      }
    }

Usando um esquema de format Django, faria:

    u = User.objects.get(id=3500401)
        .values(id, name, isViewerFriend)

    u.profilePicture = ProfilePicture.objects.get(user__id=u, size=50)
        .values(uri, width, height)

Consequentemente, para facilitar teremos algo tipo ast.wak:

    graphql.walk(ast, callback)
    def callback(node_type, **filter_by, **values):
        # ...
