#!/usr/bin/env python3
"""Genera la web de Stellaria en sus siete idiomas: /<idioma>/ (la
portada), /<idioma>/<privacidad>/ y /<idioma>/<soporte>/, con las rutas
en cada idioma, el selector de idiomas al pie y las etiquetas hreflang;
la raíz reenvía al idioma del navegador, y /privacidad/ y /soporte/ (las
rutas de la primera versión) reenvían al español.

    ./generar.py
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent
DOMINIO = "https://stellaria.games"
CORREO = "stellariajuego@gmail.com"
IDIOMAS = ["es", "en", "fr", "it", "pt-br", "de", "ja"]
NOMBRE = {"es": "Español", "en": "English", "fr": "Français", "it": "Italiano",
          "pt-br": "Português (Brasil)", "de": "Deutsch", "ja": "日本語"}
LANG = {"pt-br": "pt-BR"}   # el atributo lang y hreflang; los demás, tal cual

# --- Los textos ---------------------------------------------------------

T = {}

T["es"] = dict(
    ruta_privacidad="privacidad", ruta_soporte="soporte",
    titulo="Stellaria · poliedros y estelaciones",
    descripcion="Stellaria: un puzle de poliedros y estelaciones para iPhone y iPad. Cada estelación se monta pieza a pieza; la geometría es de verdad.",
    sub="Poliedros y estelaciones · un puzle",
    canvas="Un icosaedro girando, dibujado a tinta",
    p1="Un sólido es solo el principio. Prolonga sus caras y aparecen las estelaciones: cada una se monta pieza a pieza, girando y soltando, con la geometría de verdad debajo.",
    p2="Próximamente en la App Store, para iPhone y iPad.",
    soporte="Soporte", privacidad="Privacidad",
    priv_titulo="Política de privacidad", fecha="10 de septiembre de 2026",
    priv_resumen=("En una frase:", "Stellaria no recoge datos personales. No crea cuentas, no tiene publicidad, no lleva analíticas y no envía nada a servidores propios ni de terceros."),
    priv=[
        ("Quién es el responsable", "Stellaria es una aplicación para iPhone y iPad desarrollada y publicada por Luis Fernando Lendrino Díaz, con domicilio en España. Para cualquier cuestión sobre esta política: {correo}."),
        ("Qué datos se guardan, y dónde", "El juego guarda en tu propio dispositivo el avance (qué estelaciones has completado), tus récords y tus ajustes. Esos datos no salen del dispositivo, no llevan tu nombre ni ningún identificador personal, y se borran al desinstalar la aplicación o desde Ajustes → «Empezar de cero»."),
        ("Compras", "La compra del juego completo se hace a través de la App Store. El pago lo gestiona Apple según su propia política de privacidad; Stellaria no recibe ni conserva datos de pago, ni tu nombre, ni tu dirección. Solo sabe si la compra existe, para abrir el contenido."),
        ("Game Center", "Si decides entrar en Game Center, tus récords y logros se publican en tu cuenta de Apple para que aparezcan en sus tablas y en tu perfil. Es opcional, se apaga en Ajustes, y lo gestiona Apple según su política de privacidad. Stellaria no accede a tu lista de amigos ni a ningún otro dato de la cuenta."),
        ("Contacto por correo", "Si nos escribes desde la aplicación o desde esta web, usaremos tu dirección solo para responderte. No se añade a ninguna lista ni se comparte."),
        ("Menores", "Stellaria no recoge datos de nadie, tampoco de menores. No hay chat, ni contenido generado por usuarios, ni enlaces que salgan del juego salvo los de esta web y los de la App Store."),
        ("Tus derechos", "Como Stellaria no trata datos personales, no hay nada que rectificar, exportar ni suprimir por nuestra parte; lo que hay vive en tu dispositivo y lo controlas tú. Si aun así quieres ejercer cualquier derecho reconocido por el Reglamento General de Protección de Datos, escríbenos y te contestaremos."),
        ("Cambios", "Si alguna versión futura cambiara algo de lo anterior, esta página lo dirá con su fecha, y la aplicación enlazará siempre a la versión vigente."),
    ],
    sop_titulo="Soporte",
    sop_intro="Dudas, fallos, ideas: {correo}. Si es un fallo, cuéntanos el modelo de iPhone o iPad y qué estabas haciendo; con eso suele bastar.",
    sop_faq="Preguntas frecuentes",
    sop=[
        ("He comprado el juego completo y no aparece", "Ajustes → «Restaurar compras», con la misma cuenta de la App Store con la que compraste. Si sigue sin aparecer, escríbenos."),
        ("Quiero empezar de cero", "Ajustes → «Empezar de cero» borra el avance y los récords de ese dispositivo. No se puede deshacer."),
        ("¿Qué necesito?", "Un iPhone o un iPad con iOS 18 o iPadOS 18, o posterior."),
    ],
)

T["en"] = dict(
    ruta_privacidad="privacy", ruta_soporte="support",
    titulo="Stellaria · polyhedra and stellations",
    descripcion="Stellaria: a puzzle of polyhedra and stellations for iPhone and iPad. Every stellation is assembled piece by piece; the geometry is real.",
    sub="Polyhedra and stellations · a puzzle",
    canvas="A turning icosahedron, drawn in ink",
    p1="A solid is only the beginning. Extend its faces and the stellations appear: each one is assembled piece by piece, turning and launching, with real geometry underneath.",
    p2="Coming soon to the App Store, for iPhone and iPad.",
    soporte="Support", privacidad="Privacy",
    priv_titulo="Privacy policy", fecha="September 10, 2026",
    priv_resumen=("In one sentence:", "Stellaria collects no personal data. It creates no accounts, has no advertising, no analytics, and sends nothing to servers of its own or of third parties."),
    priv=[
        ("Who is responsible", "Stellaria is an app for iPhone and iPad developed and published by Luis Fernando Lendrino Díaz, resident in Spain. For any question about this policy: {correo}."),
        ("What data is stored, and where", "The game stores on your own device your progress (which stellations you have completed), your records and your settings. That data never leaves the device, carries no name or personal identifier, and is deleted when you uninstall the app or from Settings → “Start from scratch”."),
        ("Purchases", "The purchase of the full game is made through the App Store. Apple handles the payment under its own privacy policy; Stellaria neither receives nor keeps payment data, your name or your address. It only knows whether the purchase exists, in order to unlock the content."),
        ("Game Center", "If you choose to sign in to Game Center, your records and achievements are published to your Apple account so that they appear on its leaderboards and on your profile. It is optional, it can be turned off in Settings, and Apple handles it under its privacy policy. Stellaria does not access your friends list or any other account data."),
        ("Contact by email", "If you write to us from the app or from this website, we will use your address only to reply. It is not added to any list or shared."),
        ("Children", "Stellaria collects no data from anyone, children included. There is no chat, no user-generated content, and no links out of the game other than those to this website and to the App Store."),
        ("Your rights", "Since Stellaria processes no personal data, there is nothing for us to rectify, export or erase; what exists lives on your device and you control it. If you still wish to exercise any right recognized by the General Data Protection Regulation, write to us and we will answer."),
        ("Changes", "If a future version changed any of the above, this page would say so with its date, and the app will always link to the version in force."),
    ],
    sop_titulo="Support",
    sop_intro="Questions, bugs, ideas: {correo}. If it is a bug, tell us the iPhone or iPad model and what you were doing; that is usually enough.",
    sop_faq="Frequently asked questions",
    sop=[
        ("I bought the full game and it doesn't show up", "Settings → “Restore purchases”, with the same App Store account you bought it with. If it still doesn't show up, write to us."),
        ("I want to start from scratch", "Settings → “Start from scratch” erases the progress and records on that device. It cannot be undone."),
        ("What do I need?", "An iPhone or an iPad with iOS 18 or iPadOS 18, or later."),
    ],
)

T["fr"] = dict(
    ruta_privacidad="confidentialite", ruta_soporte="assistance",
    titulo="Stellaria · polyèdres et stellations",
    descripcion="Stellaria : un puzzle de polyèdres et de stellations pour iPhone et iPad. Chaque stellation s’assemble pièce par pièce ; la géométrie est réelle.",
    sub="Polyèdres et stellations · un puzzle",
    canvas="Un icosaèdre qui tourne, dessiné à l’encre",
    p1="Un solide n’est que le début. Prolongez ses faces et les stellations apparaissent : chacune s’assemble pièce par pièce, en tournant et en lançant, avec la vraie géométrie dessous.",
    p2="Bientôt sur l’App Store, pour iPhone et iPad.",
    soporte="Assistance", privacidad="Confidentialité",
    priv_titulo="Politique de confidentialité", fecha="10 septembre 2026",
    priv_resumen=("En une phrase :", "Stellaria ne collecte aucune donnée personnelle. Pas de compte, pas de publicité, pas de statistiques, et rien n’est envoyé à des serveurs, ni les nôtres ni ceux de tiers."),
    priv=[
        ("Qui est responsable", "Stellaria est une application pour iPhone et iPad développée et publiée par Luis Fernando Lendrino Díaz, domicilié en Espagne. Pour toute question sur cette politique : {correo}."),
        ("Quelles données sont conservées, et où", "Le jeu conserve sur votre propre appareil votre progression (les stellations que vous avez terminées), vos records et vos réglages. Ces données ne quittent pas l’appareil, ne portent ni votre nom ni aucun identifiant personnel, et sont effacées quand vous désinstallez l’application ou depuis Réglages → « Repartir de zéro »."),
        ("Achats", "L’achat du jeu complet se fait par l’App Store. Le paiement est géré par Apple selon sa propre politique de confidentialité ; Stellaria ne reçoit ni ne conserve de données de paiement, ni votre nom, ni votre adresse. Elle sait seulement si l’achat existe, pour débloquer le contenu."),
        ("Game Center", "Si vous choisissez de vous connecter à Game Center, vos records et vos succès sont publiés sur votre compte Apple pour apparaître dans ses classements et sur votre profil. C’est facultatif, cela se désactive dans les Réglages, et Apple le gère selon sa politique de confidentialité. Stellaria n’accède ni à votre liste d’amis ni à aucune autre donnée du compte."),
        ("Contact par e-mail", "Si vous nous écrivez depuis l’application ou depuis ce site, nous n’utiliserons votre adresse que pour vous répondre. Elle n’est ajoutée à aucune liste ni partagée."),
        ("Mineurs", "Stellaria ne collecte de données de personne, pas plus des mineurs. Il n’y a ni chat, ni contenu créé par les utilisateurs, ni liens sortant du jeu en dehors de ceux vers ce site et vers l’App Store."),
        ("Vos droits", "Comme Stellaria ne traite aucune donnée personnelle, il n’y a rien à rectifier, exporter ou supprimer de notre côté ; ce qui existe vit sur votre appareil et c’est vous qui le contrôlez. Si vous souhaitez malgré tout exercer un droit reconnu par le Règlement général sur la protection des données, écrivez-nous et nous vous répondrons."),
        ("Modifications", "Si une version future changeait l’un des points ci-dessus, cette page le dirait avec sa date, et l’application renverra toujours à la version en vigueur."),
    ],
    sop_titulo="Assistance",
    sop_intro="Questions, bugs, idées : {correo}. S’il s’agit d’un bug, indiquez-nous le modèle d’iPhone ou d’iPad et ce que vous faisiez ; cela suffit en général.",
    sop_faq="Questions fréquentes",
    sop=[
        ("J’ai acheté le jeu complet et il n’apparaît pas", "Réglages → « Restaurer les achats », avec le même compte App Store que celui de l’achat. S’il n’apparaît toujours pas, écrivez-nous."),
        ("Je veux repartir de zéro", "Réglages → « Repartir de zéro » efface la progression et les records de cet appareil. C’est irréversible."),
        ("De quoi ai-je besoin ?", "Un iPhone ou un iPad avec iOS 18 ou iPadOS 18, ou une version ultérieure."),
    ],
)

T["it"] = dict(
    ruta_privacidad="privacy", ruta_soporte="assistenza",
    titulo="Stellaria · poliedri e stellazioni",
    descripcion="Stellaria: un puzzle di poliedri e stellazioni per iPhone e iPad. Ogni stellazione si monta pezzo per pezzo; la geometria è vera.",
    sub="Poliedri e stellazioni · un puzzle",
    canvas="Un icosaedro che gira, disegnato a inchiostro",
    p1="Un solido è solo l’inizio. Prolunga le sue facce e compaiono le stellazioni: ognuna si monta pezzo per pezzo, girando e lanciando, con la geometria vera sotto.",
    p2="Prossimamente sull’App Store, per iPhone e iPad.",
    soporte="Assistenza", privacidad="Privacy",
    priv_titulo="Informativa sulla privacy", fecha="10 settembre 2026",
    priv_resumen=("In una frase:", "Stellaria non raccoglie dati personali. Non crea account, non ha pubblicità, non usa analitiche e non invia nulla a server propri o di terzi."),
    priv=[
        ("Chi è il titolare", "Stellaria è un’applicazione per iPhone e iPad sviluppata e pubblicata da Luis Fernando Lendrino Díaz, domiciliato in Spagna. Per qualsiasi domanda su questa informativa: {correo}."),
        ("Quali dati si conservano, e dove", "Il gioco conserva sul tuo dispositivo i progressi (quali stellazioni hai completato), i tuoi record e le tue impostazioni. Quei dati non escono dal dispositivo, non portano il tuo nome né alcun identificativo personale, e si cancellano disinstallando l’applicazione o da Impostazioni → «Ricominciare da zero»."),
        ("Acquisti", "L’acquisto del gioco completo avviene tramite l’App Store. Il pagamento lo gestisce Apple secondo la propria informativa sulla privacy; Stellaria non riceve né conserva dati di pagamento, né il tuo nome, né il tuo indirizzo. Sa soltanto se l’acquisto esiste, per sbloccare il contenuto."),
        ("Game Center", "Se decidi di accedere a Game Center, i tuoi record e i tuoi obiettivi vengono pubblicati sul tuo account Apple perché compaiano nelle sue classifiche e nel tuo profilo. È facoltativo, si disattiva nelle Impostazioni, e lo gestisce Apple secondo la sua informativa sulla privacy. Stellaria non accede alla tua lista di amici né a nessun altro dato dell’account."),
        ("Contatto via e-mail", "Se ci scrivi dall’applicazione o da questo sito, useremo il tuo indirizzo solo per risponderti. Non viene aggiunto a nessuna lista né condiviso."),
        ("Minori", "Stellaria non raccoglie dati di nessuno, nemmeno dei minori. Non ci sono chat, né contenuti generati dagli utenti, né link che escano dal gioco salvo quelli verso questo sito e verso l’App Store."),
        ("I tuoi diritti", "Poiché Stellaria non tratta dati personali, non c’è nulla da rettificare, esportare o cancellare da parte nostra; quello che esiste vive sul tuo dispositivo e lo controlli tu. Se comunque vuoi esercitare un diritto riconosciuto dal Regolamento generale sulla protezione dei dati, scrivici e ti risponderemo."),
        ("Modifiche", "Se una versione futura cambiasse qualcosa di quanto sopra, questa pagina lo dirà con la sua data, e l’applicazione rimanderà sempre alla versione in vigore."),
    ],
    sop_titulo="Assistenza",
    sop_intro="Dubbi, errori, idee: {correo}. Se è un errore, dicci il modello di iPhone o iPad e cosa stavi facendo; di solito basta.",
    sop_faq="Domande frequenti",
    sop=[
        ("Ho comprato il gioco completo e non compare", "Impostazioni → «Ripristina acquisti», con lo stesso account App Store con cui hai comprato. Se continua a non comparire, scrivici."),
        ("Voglio ricominciare da zero", "Impostazioni → «Ricominciare da zero» cancella i progressi e i record di quel dispositivo. Non si può annullare."),
        ("Cosa mi serve?", "Un iPhone o un iPad con iOS 18 o iPadOS 18, o successivo."),
    ],
)

T["pt-br"] = dict(
    ruta_privacidad="privacidade", ruta_soporte="suporte",
    titulo="Stellaria · poliedros e estelações",
    descripcion="Stellaria: um quebra-cabeça de poliedros e estelações para iPhone e iPad. Cada estelação se monta peça por peça; a geometria é de verdade.",
    sub="Poliedros e estelações · um quebra-cabeça",
    canvas="Um icosaedro girando, desenhado a tinta",
    p1="Um sólido é só o começo. Prolongue as suas faces e aparecem as estelações: cada uma se monta peça por peça, girando e lançando, com a geometria de verdade por baixo.",
    p2="Em breve na App Store, para iPhone e iPad.",
    soporte="Suporte", privacidad="Privacidade",
    priv_titulo="Política de privacidade", fecha="10 de setembro de 2026",
    priv_resumen=("Em uma frase:", "o Stellaria não coleta dados pessoais. Não cria contas, não tem publicidade, não usa análises e não envia nada a servidores próprios nem de terceiros."),
    priv=[
        ("Quem é o responsável", "O Stellaria é um aplicativo para iPhone e iPad desenvolvido e publicado por Luis Fernando Lendrino Díaz, com domicílio na Espanha. Para qualquer questão sobre esta política: {correo}."),
        ("Que dados são guardados, e onde", "O jogo guarda no seu próprio dispositivo o progresso (quais estelações você concluiu), os seus recordes e os seus ajustes. Esses dados não saem do dispositivo, não levam o seu nome nem nenhum identificador pessoal, e são apagados ao desinstalar o aplicativo ou em Ajustes → «Começar do zero»."),
        ("Compras", "A compra do jogo completo é feita pela App Store. O pagamento é gerenciado pela Apple segundo a sua própria política de privacidade; o Stellaria não recebe nem guarda dados de pagamento, nem o seu nome, nem o seu endereço. Só sabe se a compra existe, para liberar o conteúdo."),
        ("Game Center", "Se você decidir entrar no Game Center, os seus recordes e conquistas são publicados na sua conta Apple para aparecerem nas suas classificações e no seu perfil. É opcional, desliga-se nos Ajustes, e é gerenciado pela Apple segundo a sua política de privacidade. O Stellaria não acessa a sua lista de amigos nem nenhum outro dado da conta."),
        ("Contato por e-mail", "Se você nos escrever pelo aplicativo ou por este site, usaremos o seu endereço só para responder. Ele não é adicionado a nenhuma lista nem compartilhado."),
        ("Menores", "O Stellaria não coleta dados de ninguém, tampouco de menores. Não há chat, nem conteúdo gerado por usuários, nem links que saiam do jogo além dos deste site e dos da App Store."),
        ("Os seus direitos", "Como o Stellaria não trata dados pessoais, não há nada a retificar, exportar ou apagar da nossa parte; o que existe vive no seu dispositivo e é você quem controla. Se ainda assim quiser exercer qualquer direito reconhecido pela Lei Geral de Proteção de Dados ou pelo Regulamento Geral de Proteção de Dados europeu, escreva para nós e responderemos."),
        ("Alterações", "Se alguma versão futura mudar algo do que está acima, esta página dirá isso com a sua data, e o aplicativo sempre levará à versão em vigor."),
    ],
    sop_titulo="Suporte",
    sop_intro="Dúvidas, erros, ideias: {correo}. Se for um erro, conte o modelo de iPhone ou iPad e o que você estava fazendo; costuma bastar.",
    sop_faq="Perguntas frequentes",
    sop=[
        ("Comprei o jogo completo e ele não aparece", "Ajustes → «Restaurar compras», com a mesma conta da App Store com que comprou. Se continuar sem aparecer, escreva para nós."),
        ("Quero começar do zero", "Ajustes → «Começar do zero» apaga o progresso e os recordes desse dispositivo. Não é possível desfazer."),
        ("O que eu preciso?", "Um iPhone ou um iPad com iOS 18 ou iPadOS 18, ou posterior."),
    ],
)

T["de"] = dict(
    ruta_privacidad="datenschutz", ruta_soporte="support",
    titulo="Stellaria · Polyeder und Stellationen",
    descripcion="Stellaria: ein Puzzle aus Polyedern und Stellationen für iPhone und iPad. Jede Stellation wird Teil für Teil zusammengesetzt; die Geometrie ist echt.",
    sub="Polyeder und Stellationen · ein Puzzle",
    canvas="Ein sich drehendes Ikosaeder, mit Tinte gezeichnet",
    p1="Ein Körper ist nur der Anfang. Verlängere seine Flächen, und die Stellationen erscheinen: Jede wird Teil für Teil zusammengesetzt, durch Drehen und Werfen, mit echter Geometrie darunter.",
    p2="Demnächst im App Store, für iPhone und iPad.",
    soporte="Support", privacidad="Datenschutz",
    priv_titulo="Datenschutzerklärung", fecha="10. September 2026",
    priv_resumen=("In einem Satz:", "Stellaria sammelt keine personenbezogenen Daten. Es legt keine Konten an, hat keine Werbung, keine Analysen, und sendet nichts an eigene oder fremde Server."),
    priv=[
        ("Wer verantwortlich ist", "Stellaria ist eine App für iPhone und iPad, entwickelt und veröffentlicht von Luis Fernando Lendrino Díaz, wohnhaft in Spanien. Bei Fragen zu dieser Erklärung: {correo}."),
        ("Welche Daten gespeichert werden, und wo", "Das Spiel speichert auf deinem eigenen Gerät deinen Fortschritt (welche Stellationen du abgeschlossen hast), deine Rekorde und deine Einstellungen. Diese Daten verlassen das Gerät nicht, tragen weder deinen Namen noch eine persönliche Kennung, und werden gelöscht, wenn du die App deinstallierst oder unter Einstellungen → „Von vorn beginnen“."),
        ("Käufe", "Der Kauf des ganzen Spiels läuft über den App Store. Die Zahlung wickelt Apple nach seiner eigenen Datenschutzerklärung ab; Stellaria erhält und speichert weder Zahlungsdaten noch deinen Namen oder deine Adresse. Es weiß nur, ob der Kauf existiert, um den Inhalt freizuschalten."),
        ("Game Center", "Wenn du dich bei Game Center anmeldest, werden deine Rekorde und Erfolge in deinem Apple-Account veröffentlicht, damit sie in dessen Bestenlisten und in deinem Profil erscheinen. Das ist freiwillig, lässt sich in den Einstellungen abschalten und wird von Apple nach seiner Datenschutzerklärung verwaltet. Stellaria greift weder auf deine Freundesliste noch auf andere Daten des Accounts zu."),
        ("Kontakt per E-Mail", "Wenn du uns aus der App oder von dieser Website schreibst, verwenden wir deine Adresse nur, um dir zu antworten. Sie wird in keine Liste aufgenommen und nicht weitergegeben."),
        ("Minderjährige", "Stellaria sammelt von niemandem Daten, auch nicht von Minderjährigen. Es gibt keinen Chat, keine nutzergenerierten Inhalte und keine Links aus dem Spiel heraus außer denen zu dieser Website und zum App Store."),
        ("Deine Rechte", "Da Stellaria keine personenbezogenen Daten verarbeitet, gibt es bei uns nichts zu berichtigen, zu exportieren oder zu löschen; was es gibt, liegt auf deinem Gerät, und du hast die Kontrolle darüber. Wenn du dennoch ein Recht nach der Datenschutz-Grundverordnung ausüben möchtest, schreib uns, und wir antworten dir."),
        ("Änderungen", "Sollte eine künftige Version etwas davon ändern, wird diese Seite es mit Datum sagen, und die App verweist immer auf die geltende Fassung."),
    ],
    sop_titulo="Support",
    sop_intro="Fragen, Fehler, Ideen: {correo}. Wenn es ein Fehler ist, nenn uns das iPhone- oder iPad-Modell und was du gerade gemacht hast; das reicht meistens.",
    sop_faq="Häufige Fragen",
    sop=[
        ("Ich habe das ganze Spiel gekauft, und es erscheint nicht", "Einstellungen → „Käufe wiederherstellen“, mit demselben App-Store-Account, mit dem du gekauft hast. Wenn es weiterhin nicht erscheint, schreib uns."),
        ("Ich möchte von vorn beginnen", "Einstellungen → „Von vorn beginnen“ löscht Fortschritt und Rekorde auf diesem Gerät. Das lässt sich nicht rückgängig machen."),
        ("Was brauche ich?", "Ein iPhone oder ein iPad mit iOS 18 oder iPadOS 18 oder neuer."),
    ],
)

T["ja"] = dict(
    ruta_privacidad="privacy", ruta_soporte="support",
    titulo="Stellaria · 多面体と星型",
    descripcion="Stellaria：iPhoneとiPadのための、多面体と星型のパズル。星型はピースをひとつずつ組み立てます。幾何学は本物です。",
    sub="多面体と星型 · パズル",
    canvas="回転する正二十面体、インクで描いたもの",
    p1="立体は始まりにすぎません。面を延ばすと星型が現れます。ひとつひとつを、回して投げて、ピースごとに組み立てます。その下にあるのは本物の幾何学です。",
    p2="近日App Storeにて、iPhoneとiPad向けに公開予定。",
    soporte="サポート", privacidad="プライバシー",
    priv_titulo="プライバシーポリシー", fecha="2026年9月10日",
    priv_resumen=("ひとことで言うと：", "Stellariaは個人データを収集しません。アカウントを作らず、広告も分析もなく、自社や第三者のサーバーに何も送信しません。"),
    priv=[
        ("責任者", "Stellariaは、スペイン在住のLuis Fernando Lendrino Díazが開発・公開するiPhoneおよびiPad向けアプリです。このポリシーに関するお問い合わせは {correo} まで。"),
        ("保存されるデータと、その場所", "ゲームは、進行状況（どの星型を完成させたか）、記録、設定をあなたの端末内に保存します。これらのデータは端末の外に出ず、名前や個人を特定する識別子を含まず、アプリを削除するか「設定」→「はじめからやり直す」で消去されます。"),
        ("購入", "完全版の購入はApp Storeを通じて行われます。支払いはAppleが自社のプライバシーポリシーに従って処理します。Stellariaは支払い情報、氏名、住所を受け取らず、保存もしません。コンテンツを開くために、購入の有無だけを知ります。"),
        ("Game Center", "Game Centerにサインインすると、記録と実績はあなたのAppleアカウントに公開され、ランキングとプロフィールに表示されます。任意であり、「設定」でオフにでき、Appleが自社のプライバシーポリシーに従って管理します。Stellariaは友達リストやその他のアカウント情報にアクセスしません。"),
        ("メールでのお問い合わせ", "アプリやこのサイトからメールをいただいた場合、アドレスは返信のためだけに使います。リストに追加したり共有したりすることはありません。"),
        ("未成年者", "Stellariaは誰のデータも収集しません。未成年者についても同じです。チャットも、ユーザー生成コンテンツも、このサイトとApp Store以外へのリンクもありません。"),
        ("あなたの権利", "Stellariaは個人データを扱わないため、当方で訂正、書き出し、削除すべきものはありません。存在するデータはあなたの端末にあり、あなたが管理します。それでもEU一般データ保護規則などで認められた権利を行使したい場合は、ご連絡ください。お答えします。"),
        ("変更", "将来のバージョンで上記の内容が変わる場合は、このページに日付とともに記載し、アプリは常に有効なバージョンにリンクします。"),
    ],
    sop_titulo="サポート",
    sop_intro="質問、不具合、アイデアは {correo} まで。不具合の場合は、iPhoneまたはiPadの機種と、何をしていたかを教えてください。たいていはそれで十分です。",
    sop_faq="よくある質問",
    sop=[
        ("完全版を購入したのに表示されない", "「設定」→「購入を復元」を、購入したときと同じApp Storeアカウントで行ってください。それでも表示されない場合はご連絡ください。"),
        ("はじめからやり直したい", "「設定」→「はじめからやり直す」で、その端末の進行状況と記録を消去します。取り消せません。"),
        ("必要なものは？", "iOS 18またはiPadOS 18以降のiPhoneまたはiPad。"),
    ],
)

# --- Las piezas de página -----------------------------------------------

MARCA = '    <div class="marca" aria-hidden="true"></div>'


def ruta(idioma, pagina):
    """La ruta absoluta de una página en un idioma: '', 'privacidad' o 'soporte'."""
    t = T[idioma]
    tramo = {"": "", "privacidad": t["ruta_privacidad"] + "/", "soporte": t["ruta_soporte"] + "/"}[pagina]
    return f"/{idioma}/{tramo}"


def lang(idioma):
    return LANG.get(idioma, idioma)


def cabeza(idioma, pagina, titulo, descripcion=None):
    alternos = "\n".join(
        f'<link rel="alternate" hreflang="{lang(i)}" href="{DOMINIO}{ruta(i, pagina)}">' for i in IDIOMAS)
    desc = f'\n<meta name="description" content="{descripcion}">' if descripcion else ""
    return f"""<!doctype html>
<html lang="{lang(idioma)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>{desc}
<link rel="canonical" href="{DOMINIO}{ruta(idioma, pagina)}">
{alternos}
<link rel="alternate" hreflang="x-default" href="{DOMINIO}/">
<link rel="stylesheet" href="/estilo.css">
</head>
<body>
<main>"""


def idiomas(idioma, pagina):
    """El selector: la misma página en los demás idiomas, cada uno en su nombre."""
    enlaces = " · ".join(
        f'<a href="{ruta(i, pagina)}" hreflang="{lang(i)}" lang="{lang(i)}">{NOMBRE[i]}</a>'
        if i != idioma else f'<span>{NOMBRE[i]}</span>' for i in IDIOMAS)
    return f'  <p class="idiomas">{enlaces}</p>'


def correo(texto, asunto=False):
    href = f"mailto:{CORREO}" + ("?subject=Stellaria" if asunto else "")
    return texto.replace("{correo}", f'<a href="{href}">{CORREO}</a>')


def portada(idioma):
    t = T[idioma]
    return f"""{cabeza(idioma, "", t["titulo"], t["descripcion"])}
  <div class="cabecera">
    <div>
      <h1>Stellaria</h1>
      <p class="sub">{t["sub"]}</p>
    </div>
{MARCA}
  </div>

  <canvas class="solido" id="solido" width="720" height="720" aria-label="{t["canvas"]}"></canvas>

  <div class="placa">
    <p>{t["p1"]}</p>
    <p>{t["p2"]}</p>
  </div>

  <p>
    <a class="hoja" href="{ruta(idioma, "soporte")}">{t["soporte"]}</a>
    <a class="hoja" href="{ruta(idioma, "privacidad")}">{t["privacidad"]}</a>
  </p>

{idiomas(idioma, "")}
  <p class="pie">© 2026 Luis Fernando Lendrino Díaz</p>
</main>
<script src="/solido.js"></script>
</body>
</html>
"""


def privacidad(idioma):
    t = T[idioma]
    fuerte, resto = t["priv_resumen"]
    secciones = "\n\n".join(f"  <h2>{h}</h2>\n  <p>{correo(p)}</p>" for h, p in t["priv"])
    return f"""{cabeza(idioma, "privacidad", f'Stellaria · {t["priv_titulo"].lower() if idioma not in ("de", "ja") else t["priv_titulo"]}')}
  <div class="cabecera">
    <div>
      <h1>{t["priv_titulo"]}</h1>
      <p class="sub">Stellaria · {t["fecha"]}</p>
    </div>
{MARCA}
  </div>

  <div class="placa">
    <p><strong>{fuerte}</strong> {resto}</p>
  </div>

{secciones}

{idiomas(idioma, "privacidad")}
  <p class="pie"><a href="{ruta(idioma, "")}">Stellaria</a> · <a href="{ruta(idioma, "soporte")}">{t["soporte"]}</a></p>
</main>
</body>
</html>
"""


def soporte(idioma):
    t = T[idioma]
    faq = "\n\n".join(f"  <h2>{h}</h2>\n  <p>{p}</p>" for h, p in t["sop"])
    return f"""{cabeza(idioma, "soporte", f'Stellaria · {t["sop_titulo"].lower() if idioma not in ("de", "ja") else t["sop_titulo"]}')}
  <div class="cabecera">
    <div>
      <h1>{t["sop_titulo"]}</h1>
      <p class="sub">Stellaria</p>
    </div>
{MARCA}
  </div>

  <div class="placa">
    <p>{correo(t["sop_intro"], asunto=True)}</p>
  </div>

  <h2>{t["sop_faq"]}</h2>

{faq}

{idiomas(idioma, "soporte")}
  <p class="pie"><a href="{ruta(idioma, "")}">Stellaria</a> · <a href="{ruta(idioma, "privacidad")}">{t["privacidad"]}</a></p>
</main>
</body>
</html>
"""


def raiz():
    """La raíz: al idioma del navegador (los siete; el resto, inglés), y sin
    JavaScript los enlaces a todos."""
    enlaces = "\n".join(f'    <li><a href="{ruta(i, "")}" hreflang="{lang(i)}" lang="{lang(i)}">{NOMBRE[i]}</a></li>' for i in IDIOMAS)
    alternos = "\n".join(f'<link rel="alternate" hreflang="{lang(i)}" href="{DOMINIO}{ruta(i, "")}">' for i in IDIOMAS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stellaria</title>
<meta name="robots" content="noindex">
{alternos}
<link rel="alternate" hreflang="x-default" href="{DOMINIO}/">
<link rel="stylesheet" href="/estilo.css">
<script>
(function(){{
  var ok=["es","en","fr","it","pt-br","de","ja"];
  var pref=(navigator.languages||[navigator.language||"en"]).map(function(x){{return String(x).toLowerCase()}});
  for(var i=0;i<pref.length;i++){{
    var c=pref[i];
    if(c.indexOf("pt")===0){{location.replace("/pt-br/");return}}
    for(var j=0;j<ok.length;j++){{if(c===ok[j]||c.indexOf(ok[j]+"-")===0){{location.replace("/"+ok[j]+"/");return}}}}
  }}
  location.replace("/en/");
}})();
</script>
<noscript><meta http-equiv="refresh" content="0; url=/en/"></noscript>
</head>
<body>
<main>
  <div class="cabecera">
    <div>
      <h1>Stellaria</h1>
      <p class="sub">Polyhedra and stellations · a puzzle</p>
    </div>
{MARCA}
  </div>
  <ul class="lista-idiomas">
{enlaces}
  </ul>
  <p class="pie">© 2026 Luis Fernando Lendrino Díaz</p>
</main>
</body>
</html>
"""


def reenvio(destino):
    """Las rutas de la primera versión (/privacidad/, /soporte/) siguen
    respondiendo: reenvían al español."""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={destino}">
<link rel="canonical" href="{DOMINIO}{destino}">
<title>Stellaria</title>
</head>
<body><p><a href="{destino}">{DOMINIO}{destino}</a></p></body>
</html>
"""


def escribir(rel, texto):
    p = RAIZ / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto)


def main():
    for i in IDIOMAS:
        escribir(f"{i}/index.html", portada(i))
        escribir(f"{i}/{T[i]['ruta_privacidad']}/index.html", privacidad(i))
        escribir(f"{i}/{T[i]['ruta_soporte']}/index.html", soporte(i))
    escribir("index.html", raiz())
    escribir("privacidad/index.html", reenvio("/es/privacidad/"))
    escribir("soporte/index.html", reenvio("/es/soporte/"))
    print("páginas:", 3 * len(IDIOMAS) + 3)


if __name__ == "__main__":
    main()
