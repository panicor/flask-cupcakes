const BASE_URL = "http://localhost:500/api";

function makeHTML(cupcake){
    return `<div data-cupcake-id=${cupcake.id}>
        <li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}
        <button class="delete-btn btn">Delete</button>
        </li>
        <img class="cupcake-img" src="${cupcake.image}">
    </div>`;
}

async function displayCupcakes(){
    let resp = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData of resp.data.cupcakes){
        let newCupcake = $(makeHTML(cupcakeData));
        $("#cupcake-list").append(newCupcake);
    }
}

$("#new-cupcake-form").on("submit", async function (e){
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    let newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(makeHTML(newCupcakeResp.data.cupcake));
    $("#cupcake_list").append(newCupcake);
    $("new-cupcake-form").trigger("reset");
});

$("#cupcake-list").on("click", ".delete-btn", async function (e){
    e.preventDefault();

    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove()
});

$(displayCupcakes);