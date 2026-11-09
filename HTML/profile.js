const user = {
    name: 'Hedy Lamarr',
    imageUrl: 'https://imgur.com/gallery/simulation-alai2Bj',
    imageSize: 90,
  };
  
  export default function Profile() {
    return (
      <>
        <h1>{user.name}</h1>
        <img
          className="avatar"
          src={user.imageUrl}
          alt={'Foto de ' + user.name}
          style={{
            width: user.imageSize,
            height: user.imageSize
          }}
        />
      </>
    );

    
  }