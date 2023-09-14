const isProduction = process.env.REACT_APP_ENV === 'prod';

const globals = {
    SERVER: isProduction ? 'http://localhost:8000' : 'http://localhost:8000',
    IMAGES_API: '/api/v1/images/',
    DOWNLOAD_API: '/api/v1/download/',
    TEST_DATA: [
        {
            "id": 252,
            "png_image": "/media/PNGs/sonic_test_yeUQRbP.png",
            "image_name": "sonic_test.png",
            "status": "SUCCESS"
        },
        {
            "id": 254,
            "png_image": "/media/PNGs/The_death_test_iCoPoN1.png",
            "image_name": "The_death_test.png",
            "status": "SUCCESS"
        },
        {
            "id": 255,
            "png_image": "/media/PNGs/dice_test_LQ7xXqv.png",
            "image_name": "dice_test.png",
            "status": "SUCCESS"
        },
        {
            "id": 253,
            "png_image": "/media/PNGs/mario_test_ytK7i1u.png",
            "image_name": "mario_test.png",
            "status": "SUCCESS"
        }
    ],
};

export default globals;