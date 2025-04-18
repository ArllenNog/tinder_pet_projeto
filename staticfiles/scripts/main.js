$(document).ready(()=>{
    $("input[name='telefone']").mask('(00) 00000-0000');
    $("input[name='whatsapp']").mask('(00) 00000-0000');
    $(".viewer").css("height", $(".viewer").width());
});

$("#intro-adotar-btn").click(()=>{
    //$("#intro-screen").remove();
    $("#quer-adotar-ipt").val(1);
    $("#first-form").submit();
});

$("#intro-doar-btn").click(()=>{
    //$("#intro-screen").remove();
    $("#first-form").submit();
});

$("#intro-apoiar-btn").click(()=>{
    $("#quer-apoiar-ipt").val(1);
    $("#first-form").submit();
});

$("#filtro-cachorros").click( () =>{
    $("#filtro-tipo").val(0);
    $("#filtro-form").submit();
});

$("#filtro-gatos").click( () =>{
    $("#filtro-tipo").val(1);
    $("#filtro-form").submit();
});

$("#filtro-todos").click( () =>{
    $("#filtro-tipo").val(2);
    $("#filtro-form").submit();
});

$("#tel-numero").on("input", ()=>{
    if($("#whatsapp-check").is(":checked")){
        $("#whatsapp-numero").val($("#tel-numero").val());
    }
})

$("#whatsapp-check").on("change", ()=>{
    if($("#whatsapp-check").is(":checked")){
        $("#whatsapp-numero").val($("#tel-numero").val());
        $("#whatsapp-numero").prop("readonly", true);
        $("#whatsapp-numero").css('background-color', 'white');
    }
    else
    {
        $("#whatsapp-numero").val("");
        $("#whatsapp-numero").prop("readonly", false);
    }
});

$("#btn-entrar-email").click(()=>{
    $("#tela1").addClass("visually-hidden");
    $("#tela2").removeClass("visually-hidden");
});

$("#btn-voltar-login").click(()=>{
    $("#tela2").addClass("visually-hidden");
    $("#tela1").removeClass("visually-hidden");
});

$("#meu-dados-btn").click(()=>{
    ativarMenuBtn("#meu-dados-btn");
    ativarCards(["#card-minha-pagina", "#card-informacoes", "#card-contato"]);
});

$("#meus-anuncios-btn").click(()=>{
    ativarMenuBtn("#meus-anuncios-btn");
    ativarCards(["#card-meus-anuncios"]);
});

$("#meus-pets-btn").click(()=>{
    ativarMenuBtn("#meus-pets-btn");
    ativarCards(["#card-meus-pets"]);
});

$("#notificacoes-btn").click(()=>{
    ativarMenuBtn("#notificacoes-btn");
    ativarCards(["#card-notificacoes"]);
});

$("#pet-tipo-radio-cachorro").change(()=>{
    $("#racas-gatos").hide();
    $("#racas-cachorros").show();
});

$("#pet-tipo-radio-gato").change(()=>{
    $("#racas-cachorros").hide();
    $("#racas-gatos").show();
});

$("#foto-destaque-pet").change(function(event){
    loadImage(event, "#foto-destaque-pet-target","#foto-destaque-pet-label");
});
$("#foto-1-pet").change(function(event){
    loadImage(event, "#foto-1-pet-target","#foto-1-pet-label");
});
$("#foto-2-pet").change(function(event){
    loadImage(event, "#foto-2-pet-target","#foto-2-pet-label");
});
$("#foto-3-pet").change(function(event){
    loadImage(event, "#foto-3-pet-target","#foto-3-pet-label");
});
$("#foto-4-pet").change(function(event){
    loadImage(event, "#foto-4-pet-target","#foto-4-pet-label");
});

$("#btn-remove-foto-destaque-pet").click(()=>{
    removeImage("#foto-destaque-pet", "#foto-destaque-pet-preview", "#foto-destaque-pet-label" );
});
$("#btn-remove-foto-1-pet").click(()=>{
    removeImage("#foto-1-pet", "#foto-1-pet-preview", "#foto-1-pet-label");
    $("input[name='delete_foto_1']").attr("value", "1");
});
$("#btn-remove-foto-2-pet").click(()=>{
    removeImage("#foto-2-pet", "#foto-2-pet-preview", "#foto-2-pet-label" );
    $("input[name='delete_foto_2']").attr("value", "1");
});
$("#btn-remove-foto-3-pet").click(()=>{
    removeImage("#foto-3-pet", "#foto-3-pet-preview", "#foto-3-pet-label" );
    $("input[name='delete_foto_3']").attr("value", "1");
});
$("#btn-remove-foto-4-pet").click(()=>{
    removeImage("#foto-4-pet", "#foto-4-pet-preview", "#foto-4-pet-label" );
    $("input[name='delete_foto_4']").attr("value", "1");
});

$("#modal-exclusao").submit(()=>{
    //excluir entrada
    $("#form-exclusao2").submit();
});

$("#btn-cancel-modal-exclusao").click(()=>{
    $("#aviso-exclusao")[0].close();
});


function loadImage(event, target, label){
    if (event.target.files && event.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          $(target).prop("src", e.target.result);
          $(target).parent().css("display", "block");
          $(label).hide();
          $(".viewer").children().attr("src", e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
        $("#anuncio-btn-salvar").show();
    }
}

function removeImage(input, viewer, btn)
{
    $(input).val('');
    $(viewer).hide();
    $(btn).show();
    $("#anuncio-btn-salvar").show();
}

function ativarMenuBtn(target){
    $("#meu-dados-btn").removeClass("selected-fill");
    $("#meu-dados-btn-icon").css("fill", "#5ab031");
    $("#meus-anuncios-btn").removeClass("selected-fill");
    $("#meus-anuncios-btn-icon").css("fill", "#5ab031");
    $("#notificacoes-btn").removeClass("selected-fill");
    $("#notificacoes-btn-icon").css("fill", "#5ab031");

    $(target).addClass("selected-fill");
    $(target+"-icon").css("fill", "white");
}

function ativarCards(targets){
    $("#card-minha-pagina").hide();
    $("#card-informacoes").hide();
    $("#card-contato").hide();
    $("#card-meus-anuncios").hide();
    $("#card-meus-pets").hide();
    $("#card-notificacoes").hide();

    targets.forEach((card) => {
        $(card).show();
    });
}


function openWhatsApp(numero, nome, tipo) {
    numero = numero.replace(/\D/g, '');//limpar tracos e parenteses
    numero = "55"+numero;//formatar para whatsapp
    var message = "";
    var whatsappUrl = "";
    if(tipo == 0){
        message = encodeURIComponent(`Olá, vi o anúncio do seu pet *${nome}* no site do *Tinder Pet* e tenho interesse em adotá-lo. 🐾🏠`);
        whatsappUrl = `https://api.whatsapp.com/send?phone=${numero}&text=${message}`;
    }
    else
    {
        message = encodeURIComponent(`Olá, vi o anúncio do seu pet *${nome}* no site do *Tinder Pet* e tenho um(a) parceiro(a) disponível para o cruzamento. 🐾❤️`);
        whatsappUrl = `https://api.whatsapp.com/send?phone=${numero}&text=${message}`;
    }
    
    // Redireciona para o WhatsApp
    window.open(whatsappUrl, '_blank');
    //envia o form
}

$(".photo-item").click((event)=>{
    $(".viewer").children().attr("src", $(event.target).children().attr("src"));
    $(".photo-item").removeClass("selected");
    $(event.target).addClass("selected");
});

//desativar foco de aviso para os campos
$(".tinder-pet-input").change(function(){
    $(this).css('background-color', 'white');
});

//desativar foco de aviso para os campos de seleção de icones
$(".ipt-group1").change(function(){
    $(".lbl-group1").css('background-color', 'transparent');
});

$(".ipt-group2").change(function(){
    $(".lbl-group2").css('background-color', 'transparent');
});

//desativar foco do botao de upload de foto do pet
$("#foto-destaque-pet").change(function(){
    $("#foto-destaque-pet-label").css('border', 'none');
});

/* --------------------------------------*/
/* FUNCOES DE EDICAO INFORMACOES BASICAS */
/* --------------------------------------*/
$("#info-edit-btn").click(()=>{
    $("#info-edit-btn").hide();
    $("#info-save-btn").show();
    $("#info-cancel-btn").show();
    $(".info-edit-input").show();
    $(".info-view").hide();
    $("#info-nome-ipt").val($("#info-view-nome").text());
    //$("#info-email-ipt").val($("#info-view-email").text());
    $("#info-senha-ipt").val($("#info-view-senha").text());
});

$("#info-cancel-btn").click(()=>{
    $("#info-edit-btn").show();
    $("#info-save-btn").hide();
    $("#info-cancel-btn").hide();
    $(".info-edit-input").hide();
    $(".info-view").show();
});

$("#info-edit-btn2").click(()=>{
    $("#info-edit-btn2").hide();
    $("#info-save-btn2").show();
    $("#info-cancel-btn2").show();
    $(".info-edit-input2").show();
    $(".info-view2").hide();
    $("#info-bairro-ipt").val($("#info-view-bairro").text());
    $("#info-cidade-ipt").val($("#info-view-cidade").text());
    $("#info-telefone-ipt").val($("#info-view-telefone").text());
    $("#info-whatsapp-ipt").val($("#info-view-whatsapp").text());
});

$("#info-cancel-btn2").click(()=>{
    $("#info-edit-btn2").show();
    $("#info-save-btn2").hide();
    $("#info-cancel-btn2").hide();
    $(".info-edit-input2").hide();
    $(".info-view2").show();
});

/* -----------------------------*/
/* FUNCOES DE EDICAO DO ANUNCIO */
/* -----------------------------*/

var editing_texto = false;
$("#anuncio-edit-btn-texto").click(()=>{
    editing_texto = atualizarCampos(editing_texto, "#anuncio-view-texto", "#anuncio-ipt-texto","#anuncio-edit-icon-texto", "#anuncio-save-icon-texto", "#anuncio-btn-salvar");
});

var editing_peso = false;
$("#anuncio-edit-btn-peso").click(()=>{
    editing_peso = atualizarCampos(editing_peso, "#anuncio-view-peso", "#anuncio-ipt-peso","#anuncio-edit-icon-peso", "#anuncio-save-icon-peso", "#anuncio-btn-salvar");
});

var editing_idade = false;
$("#anuncio-edit-btn-idade").click(()=>{
    editing_idade = atualizarCampos(editing_idade, "#anuncio-view-idade", "#anuncio-ipt-idade","#anuncio-edit-icon-idade", "#anuncio-save-icon-idade", "#anuncio-btn-salvar");
});

var editing_bairro = false;
$("#anuncio-edit-btn-bairro").click(()=>{
    editing_bairro = atualizarCampos(editing_bairro, "#anuncio-view-bairro", "#anuncio-ipt-bairro","#anuncio-edit-icon-bairro", "#anuncio-save-icon-bairro", "#anuncio-btn-salvar");
});

var editing_cidade = false;
$("#anuncio-edit-btn-cidade").click(()=>{
    editing_cidade = atualizarCampos(editing_cidade, "#anuncio-view-cidade", "#anuncio-ipt-cidade","#anuncio-edit-icon-cidade", "#anuncio-save-icon-cidade", "#anuncio-btn-salvar");
});

/* EDICAO DA PAGINA DA ONG */
var editing_nome_ong = false;
$("#ong-edit-btn-nome").click(()=>{
    editing_nome_ong = atualizarCampos(editing_nome_ong, "#ong-view-nome", "#ong-ipt-nome","#ong-edit-icon-nome", "#ong-save-icon-nome", "#ong-btn-salvar");
});


function atualizarCampos(is_editing, view, ipt, editIcon, saveIcon, btnSalvar){
    if(!is_editing)
    {
        $(view).hide();
        $(ipt).prop("hidden", false);
        if($(view).text().trim() != "Sem dado")
            $(ipt).val( $(view).text() );
        else
            $(ipt).val('');
        $(ipt).focus()
        $(editIcon).hide();
        $(saveIcon).show();
        $(btnSalvar).show();
        is_editing = true;
    }
    else
    {
        if($(ipt).val().length > 0)
            $(view).text($(ipt).val());
        else
            $(view).text("Sem dado");
        $(view).show();
        $(ipt).prop("hidden", true);
        $(editIcon).show();
        $(saveIcon).hide();
        is_editing = false;
    }

    return is_editing;
}

/*$("#anuncio-btn-ver").click(()=>{
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search);

    // Define o novo valor do parâmetro 'viewMode'
    params.set('viewMode', '1'); // Altere '2' para o valor desejado

    // Atualiza a URL e recarrega a página
    url.search = params.toString();
    window.location.href = url.toString();

});

$("#anuncio-btn-editar").click(()=>{
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search);

    // Define o novo valor do parâmetro 'viewMode'
    params.set('viewMode', '0'); // Altere '2' para o valor desejado

    // Atualiza a URL e recarrega a página
    url.search = params.toString();
    window.location.href = url.toString();

});*/

$("#anuncio-btn-excluir").click(()=>{
    $("#aviso-exclusao")[0].showModal();
});

$("#anuncio-btn-adotar").click(()=>{
    $("#form-doacao").submit();
    openWhatsApp($("#anunciante-tel-ipt").val(), $("#pet-nome-ipt").val(), $("#anuncio-tipo-ipt").val());
});

$(".confirma-adocao-btn").click(function(){
    $("input[name='id_adotante']").attr("value", $(this).attr("data-id"));
    $("#form-concluir").submit();
});

$("#anuncio-btn-adotar2").click(()=>{
    openWhatsApp($("#anunciante-tel-ipt").val(), $("#pet-nome-ipt").val(), $("#anuncio-tipo-ipt").val());
});


$("#anuncio-btn-finalizar").click(()=>{
    $("input[name='desativar']").attr("value", "1");
    $("#form-desativar").submit();
});

$("#anuncio-btn-reativar").click(()=>{
    $("input[name='desativar']").attr("value", "0");
    $("#form-desativar").submit();
});

$("#cadastro-enviar-btn").click(validarCamposCadastro);
//$("#novo-pet-enviar-btn").click(validarCamposNovoPet);
$("#novo-anuncio-enviar-btn").click(validarCamposAnuncio);

function validarCamposCadastro(){
    var podeEnviar = true;

    //verificar campo nome
    if ($("input[name='nome']").val().length < 3 ){
        $("input[name='nome']").css('background-color', 'yellow');
        podeEnviar = false;
    }
    
    //verificar campo email
    var txtEmail = $("input[name='email']").val();
    if (txtEmail.length < 5 && !txtEmail.includes("@")){
        $("input[name='email']").css('background-color', 'yellow');
        podeEnviar = false;
    }
    
    //verificar campo senha
    var txtSenha = $("input[name='senha']").val();
    if(txtSenha.length < 4){
        $("input[name='senha']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //senhas não concidem
    var txtSenha2 = $("input[name='senha2']").val();
    if(txtSenha2 !== txtSenha){
        $("input[name='senha2']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar campo bairro
    if ($("input[name='bairro']").val().length < 3 ){
        $("input[name='bairro']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar se alguma cidade foi selecionada
    if(!$("select[name='cidade']").val())
    {
        $("select[name='cidade']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar telefone
    if($("input[name='telefone']").val().length < 11)
    {
        $("input[name='telefone']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar whatsapp
    if($("input[name='whatsapp']").val().length < 11)
    {
        $("input[name='whatsapp']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    if(podeEnviar)
        $("#cadastro-form").submit();
    else
        $("#aviso")[0].showModal();
}

/*function validarCamposNovoPet(){
    var podeEnviar = true;
    var tipopet = 0;

    //verificar campo tipo de pet
    if (!$("input[name='pet_tipo']:checked").val())
    {
        $(".lbl-group1").css('background-color', 'yellow');
        podeEnviar = false;
    }
    else
    {
        tipopet = parseInt( $("input[name='pet_tipo']:checked").val());
    }

    //verificar campo de sexo
    if (!$("input[name='pet_sexo']:checked").val())
    {
        $(".lbl-group2").css('background-color', 'yellow');
        podeEnviar = false;
    }
    

    if(tipopet == 0){
        //verificar campo de raça (cachorro)
        if(!$("select[name='raca_pet_id_cachorro']").val())
        {
            $("select[name='raca_pet_id_cachorro']").css('background-color', 'yellow');
            podeEnviar = false;
        }
    }
    else
    {
        //verificar campo de raça (gato)
        if(!$("select[name='raca_pet_id_gato']").val())
        {
            $("select[name='raca_pet_id_gato']").css('background-color', 'yellow');
            podeEnviar = false;
        }
    }

    //verificar campo nome
    if ($("input[name='nome_pet']").val().length < 2 ){
        $("input[name='nome_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }
    
    //verificar campo de peso
    if (!$("input[name='peso_pet']").val())
    {
        $("input[name='peso_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar campo de idade
    if (!$("input[name='idade_pet']").val())
    {
        $("input[name='idade_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar se subiu pelo menos a foto principal
    if (!$("input[name='foto_destaque']").val())
    {
        $("#foto-destaque-pet-label").css('border', 'solid 6px yellow');
        podeEnviar = false;
    }

    if(podeEnviar)
        //$("#form-novo-pet").submit();
        $("#form-novo-pet").submit();
    else
        $("#aviso")[0].showModal();
}*/

function validarCamposAnuncio(){
    var podeEnviar = true;

    //verificar campo de tipo de anuncio
    /*if (!$("input[name='anuncio_tipo']:checked").val())
    {
        $(".lbl-group1").css('background-color', 'yellow');
        podeEnviar = false;
    }*/

    //verificar campo de selecao de pet
    /*if (!$("input[name='pet_id']:checked").val())
    {
        $(".lbl-group2").css('background-color', 'yellow');
        podeEnviar = false;
    }*/

    //verificar campo titulo
    /*if ($("input[name='titulo']").val().length < 3 ){
        $("input[name='titulo']").css('background-color', 'yellow');
        podeEnviar = false;
    }*/

    var tipopet = 0;

    //verificar campo tipo de pet
    if (!$("input[name='pet_tipo']:checked").val())
    {
        $(".lbl-group1").css('background-color', 'yellow');
        podeEnviar = false;
    }
    else
    {
        tipopet = parseInt( $("input[name='pet_tipo']:checked").val());
    }

    if(tipopet == 0){
        //verificar campo de raça (cachorro)
        if(!$("select[name='raca_pet_id_cachorro']").val())
        {
            $("select[name='raca_pet_id_cachorro']").css('background-color', 'yellow');
            podeEnviar = false;
        }
    }
    else
    {
        //verificar campo de raça (gato)
        if(!$("select[name='raca_pet_id_gato']").val())
        {
            $("select[name='raca_pet_id_gato']").css('background-color', 'yellow');
            podeEnviar = false;
        }
    }

    //verificar campo de sexo
    if (!$("input[name='pet_sexo']:checked").val())
    {
        $(".lbl-group2").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar campo nome
    if ($("input[name='nome_pet']").val().length < 2 ){
        $("input[name='nome_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }
    
    //verificar campo de peso
    if (!$("input[name='peso_pet']").val())
    {
        $("input[name='peso_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar campo de idade
    if (!$("input[name='idade_pet']").val())
    {
        $("input[name='idade_pet']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar campo descricao
    if ($("textarea[name='desc']").val().length < 3 ){
        $("textarea[name='desc']").css('background-color', 'yellow');
        podeEnviar = false;
    }

    //verificar se subiu pelo menos a foto principal
    if (!$("input[name='foto_destaque']").val())
    {
        $("#foto-destaque-pet-label").css('border', 'solid 6px yellow');
        podeEnviar = false;
    }

    if(podeEnviar)
        $("#novo-anuncio-form").submit();
    else
        $("#aviso")[0].showModal();
}