from .models import *
from rest_framework import serializers, fields


class AlbumSerializer(serializers.ModelSerializer):

    id = serializers.ModelField(model_field=Album()._meta.get_field('id'),required=False,allow_null=True)
    class Meta:
        model = Album
        fields = ('id', 'artist', 'name', 'release_date', 'num_stars')


class MusicianSerializer(serializers.ModelSerializer):
    album_musician = AlbumSerializer(many=True)

    class Meta:
        model = Musician
        fields = ('id', 'first_name', 'last_name', 'instrument', 'album_musician')

    def create(self, validated_data):
        albums_data = validated_data.pop('album_musician')
        musician = Musician.objects.create(**validated_data)
        for album_data in albums_data:
            Album.objects.create(artist=musician, **album_data)
        return musician

    # def update(self, instance, validated_data):
    #     albums_data = validated_data.pop('album_musician')
    #     albums = (instance.album_musician).all()
    #     albums = list(albums)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.instrument = validated_data.get('instrument', instance.instrument)
    #     instance.save()
    #
    #     # for item in albums:
    #     #     print(item.name)
    #     #     print(item.release_date)
    #     #     print(item.artist)
    #
    #
    #     print(albums_data)
    #
    #     album_ids=list()
    #     for album_item in albums_data:
    #         album_ids.append(album_item['artist'])
    #
    #     print(album_ids)
    #     for item in albums:
    #             if item.artist not in album_ids:
    #                 item.delete()
    #
    #     for album_data in albums_data:
    #         album = albums.pop(0)
    #         album.artist = album_data.get('artist', album.artist)
    #         album.name = album_data.get('name', album.name)
    #         album.release_date = album_data.get('release_date', album.release_date)
    #         album.num_stars = album_data.get('num_stars', album.num_stars)
    #         album.save()
    #     return instance

    def update(self, instance, validated_data):
        albums_data = validated_data.pop('album_musician')
        albums = (instance.album_musician).all()
        albums = list(albums)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.instrument = validated_data.get('instrument', instance.instrument)
        instance.save()


        album_ids=list()
        for album_id in albums_data:
            if album_id['id']:
                album_ids.append(album_id['id'])

        album_instances_ids = list()
        for album in albums:
            album_instances_ids.append(album.id)

        updateable_ids=list(set(album_ids)&set(album_instances_ids))
        print(updateable_ids)


        deleteable_ids=list(set(album_instances_ids)-set(album_ids))
        print(deleteable_ids)



        for album_data in albums_data:

            if album_data['id'] in updateable_ids:
                    album = Album.objects.get(pk=album_data['id'])

                    album.name = album_data.get('name', album.name)
                    album.release_date = album_data.get('release_date', album.release_date)
                    album.num_stars = album_data.get('num_stars', album.num_stars)
                    album.save()
            elif album_data['id'] is None:
                Album.objects.create(artist_id=instance.id, **album_data)

        for delete_id in deleteable_ids:
                    album = Album.objects.get(pk=delete_id)
                    album.delete()

        return instance




