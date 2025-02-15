PGDMP     5                
    y            akiba    13.1    13.1 #    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    32864    akiba    DATABASE     i   CREATE DATABASE akiba WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE akiba;
                postgres    false            �            1259    32865    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    57474    deposits    TABLE     �   CREATE TABLE public.deposits (
    ref_no character varying(15) NOT NULL,
    id_no integer,
    date character varying(100),
    amount character varying(100)
);
    DROP TABLE public.deposits;
       public         heap    postgres    false            �            1259    65668    inactive_users    TABLE     e   CREATE TABLE public.inactive_users (
    id integer NOT NULL,
    username character varying(100)
);
 "   DROP TABLE public.inactive_users;
       public         heap    postgres    false            �            1259    65666    inactive_users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.inactive_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.inactive_users_id_seq;
       public          postgres    false    208            �           0    0    inactive_users_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.inactive_users_id_seq OWNED BY public.inactive_users.id;
          public          postgres    false    207            �            1259    32872    roles    TABLE     \   CREATE TABLE public.roles (
    id integer NOT NULL,
    role_name character varying(50)
);
    DROP TABLE public.roles;
       public         heap    postgres    false            �            1259    32870    roles_id_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.roles_id_seq;
       public          postgres    false    202            �           0    0    roles_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;
          public          postgres    false    201            �            1259    49289    transactions    TABLE     �   CREATE TABLE public.transactions (
    ref_no character varying(100) NOT NULL,
    id_no integer,
    date character varying(100),
    deposit character varying(100),
    withdrawal character varying(100),
    status character varying(100)
);
     DROP TABLE public.transactions;
       public         heap    postgres    false            �            1259    32880    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    firstname character varying(100),
    lastname character varying(100),
    username character varying(100),
    password character varying(100),
    account_balance double precision,
    float_balance integer,
    role_id integer,
    phone character varying(100),
    pin character varying(100),
    profile_pic character varying(100),
    notification character varying(100),
    "userID" integer
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    32878    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    204            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    203            >           2604    65671    inactive_users id    DEFAULT     v   ALTER TABLE ONLY public.inactive_users ALTER COLUMN id SET DEFAULT nextval('public.inactive_users_id_seq'::regclass);
 @   ALTER TABLE public.inactive_users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    208    207    208            <           2604    32875    roles id    DEFAULT     d   ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);
 7   ALTER TABLE public.roles ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    202    201    202            =           2604    32883    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    204    203    204            �          0    32865    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    200   &       �          0    57474    deposits 
   TABLE DATA           ?   COPY public.deposits (ref_no, id_no, date, amount) FROM stdin;
    public          postgres    false    206   8&       �          0    65668    inactive_users 
   TABLE DATA           6   COPY public.inactive_users (id, username) FROM stdin;
    public          postgres    false    208   �&       �          0    32872    roles 
   TABLE DATA           .   COPY public.roles (id, role_name) FROM stdin;
    public          postgres    false    202   +'       �          0    49289    transactions 
   TABLE DATA           X   COPY public.transactions (ref_no, id_no, date, deposit, withdrawal, status) FROM stdin;
    public          postgres    false    205   a'       �          0    32880    users 
   TABLE DATA           �   COPY public.users (id, firstname, lastname, username, password, account_balance, float_balance, role_id, phone, pin, profile_pic, notification, "userID") FROM stdin;
    public          postgres    false    204   G)       �           0    0    inactive_users_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.inactive_users_id_seq', 1, false);
          public          postgres    false    207            �           0    0    roles_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.roles_id_seq', 3, true);
          public          postgres    false    201            �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 9, true);
          public          postgres    false    203            @           2606    32869 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    200            H           2606    57478    deposits deposits_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.deposits
    ADD CONSTRAINT deposits_pkey PRIMARY KEY (ref_no);
 @   ALTER TABLE ONLY public.deposits DROP CONSTRAINT deposits_pkey;
       public            postgres    false    206            J           2606    65673 "   inactive_users inactive_users_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.inactive_users
    ADD CONSTRAINT inactive_users_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.inactive_users DROP CONSTRAINT inactive_users_pkey;
       public            postgres    false    208            B           2606    32877    roles roles_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public            postgres    false    202            F           2606    49303    transactions transactions_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (ref_no);
 H   ALTER TABLE ONLY public.transactions DROP CONSTRAINT transactions_pkey;
       public            postgres    false    205            D           2606    32885    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    204            K           2606    32886    users users_role_id_fkey    FK CONSTRAINT     w   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_role_id_fkey;
       public          postgres    false    204    2882    202            �      x�352407703H56����� "�N      �      x�}�1�0D��>�O@ffm�u�"Q�HA���P�,%韾��l�`V+�# O�$���ITgK�9 .+[����޳�sح\a߰���ŁPO�t��l`�ṝ0;�öc��6\��c���6�      �   T   x�%��
�  �����V��R4�l����q�1����ph�%]��D/>
$�֬DOȽ"�K���V��A�aG#�a�ߣ�N��)�      �   &   x�3�LL����2�LLO�+�2��M�MJ-����� ��      �   �  x���;n�@�Z{�=A��I�C�a�` E��E�����)|�>��8�E�{�H܃��?>�V�����ey�~}}{>o�I	X'J0VѦ*��-bq�t��0Q�M�B�dUw��)
&ʓX&�X~��[��X�F�3�%$�P�+�M���'�v��]^I�B��pY�uyS�U*<�KtSV!�\��J��D��<�O�+dS	�/t0��1��E�X.�Z��;JXfJ�JA�p�JG���3e��7��c�0(��"�R��4L� �F��&�r��'���PZ*��a;ּPɋ^)�J{^ܮ��T�*w��.sj{Y�NY>7͑Jl+�*R��<��2�b���}UC^i?��b��)q���㫕���@��V�Q��ˊX�R�� J���L�ϧ�Q 	�����e1)U:��2�F�=�J��1Q��L�EL�da;R���M�J����-"�V��B7R�n��-i�'      �   �  x��X�r��]�~��}B�YKЄ�I/�CCi@B|��طo���Y,�Nf��<e�`@��i:xN}�b@���w�/<��u�03Uf���q�2z��%��A�F�iW�۔;^�k���B�!p
%��0 �q�$I�{95��	���[�6kwydit�$���%(��m3��lK�	��nm�V+��7�X��)0�p$��,��C�k��pc1$�k8GT5O���>�_W�.���l�������!
V����{�Ѵ[lO��+W̪#���1�&�N%�ؐ�8�q�Ӆu���,��~dH��,o�R�{���C ��D0���G��7�,��z�\�US�~����k2Yټ.-��w�����SF����E��5zрP���6_���dc��ʊ�<��h�}�c�QX�X���/g_��k������>�^��L_�5|񺿦��+��p�?����H>�� ɟ�����ja�;2'�����D�=_M�b�7���),(;I|�Y�B�za���M%¢3����d{T]�r���{�g�A߶�->
�`G��"�9+��J`O��?�?>�#x�GT*�\��`If�m�ŰG����s�+�R�a�[��b�#z	-���n��7p^�;�P"�9��7�zq����q�]H����=����Z#�ߧ����u�a�)��Ҳ��`��i��i}���(Q��M�]���Ɂ���p�_\�� X�>1毊�-Z�f`�j�Ӊz�Sfa��}m.IW�R"�j]�ki����אl��7
�,�������;�o3D}ތ�ᕻM��Kv��vۊ���.S�RD���&e���[4��rՒZg�I��p�˝��'�qK��$���Ed�U�Ɩ/M����^L�����1����H� 璯`�����%̐ ��l��ʅ�ޏ��h�Z|R�ԨL�:���E�-	i �<M��L�?:��?��l����s܋o��Y�p���W׀^�i���K�:cf1�v�W?A q���>&��������u=�%���)}Ӓ�i%SC�_w�Bb�]��%�Z�'@ew�B � �%^!���c�xH[ʪ�#Уe�6aaGw���M�q����m0�ts=�V��%���?B86�[�_�[�M��0zS�}#)���o~��M�>G�8�~��!|˺�/��B�8�D���9�>�:�|����G2f��6Ptvذ;:�Ʉ�:�q�zXd�=����K��
��)q����Gȗ������(�	HC?�J6�'R5Q�^���m�Ӱ�TzkE,�4�;RH{�0�����!{�~�0{���P�).����mGig�h�/�ɺ���J@Im:��>�_��s���j�j���(�D���2A뮹���
FA��"Uyg*�kd�����9|�����u�	��.+�y&�&r�煑���:̰��x(�Éw�s ��m��[kw1Yth�r����
6�~����z��r�]6�.���,�U�}iȥW_�������Ex�hT����8Ѧ(���N*�g#͗]t������.�st �+�Y�B�$�{E�{/И�&2i�x���]��͐� o��]F�
4�B�����.P�JvqJ��o���R�n˓튐��?���߭4D*"̥�:D�*����uSdՋ��\G��;��ݢ!x�LP������T�*���+笹�Q�Ϝ?�6KS3_G-���Q�d}��@�`���1+��A�˰�y~	j�<**����]-s�:�C!?YG��eЗ��R��Qt3A�2fa��Y/?<[{k�9@��@�i%�4��P�#Q�#��^Gɐ#�k�aC�W��7fmwK����:\���y-���E�E՗8�0g���S��@t؆��U0�
�q������x1��'�XK�^?;�P]0�S�$uȚ��y}䩭���!/�!1��cA}�2�-����Xw����98�G��a��yeP*[�6U�Nt����@��	b�������;��*?��o>r(����N��R��Iz�_��k���͸HĕO�p�@�!\��[�g?J5.�Чc� �]OqZ�#�y��{��2� "�x�9`����������{�匿)�x|�էJ����2q,5H&%K�E��^'�r�i��5N�bl�(�[Ig����y�`M}�����A ����e]�7)��b�k�Sw����j�R.\o3����$��Ԝ��J���<�f�	����%נּ~�/�m).�eC�+ӽ-���2rp� �g��P;����m�)ڞg�YdD�q�L�n(l����I����@�aD�2B:��.����V�0�^+���A�Cx���pôއ�j:�u�ռ3l]��_&��4��kﴂү���Ĳܼ�I�厠���/��������Kj�\_��x����,H#���q%������b�O�d�gI=�����G�6�>�Uj�1��	٫z��[,p�/���C��-��������$����ŉOᝲ���Ʋ��P>4]��)Wo�Ԝ0j`G\R�>[fq�ԁ]Wӿ�s��M��~�W~���ۻ�j_6�)C[�l��km)�]*���U����\S6ʒ�o�ҺB�`����2�y���f(�'���,Zr�����5@�7�Q[��"�/��<��K��x�Ffe�GƑVM�ٹ��:�
N�3��*:��i��"a�:�\��66u�d�:\Ά�����=m��άO+Kj�@bNþ���j�G��y�:a��x���&�?�����o��ߞ��뺳�TѴؖ����5�x�{��z����]['fp���M�-����Y��%�<��M�9tw|!��r�Y�MS�!9idY�2�W������+�8"��~���������QwQsW��c��*�	����Z�6���V٬}^,�J�c�$2��7#��'�%ʾ\��,�38�Ve�W/�E�\�a/�sݍ]-U��a����e����WB���:ƿ���_�~�8ʺ     