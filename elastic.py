from flask import request
from app import es
from elasticsearch_dsl import Search, Q
from helpers import float_from_request, bool_from_request


class Elastic(object):
    index = 'test_index'

    def sync_project_document(self, project):
        project_doc = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "price": project.price,
            "published": project.published,
            "location": "%s,%s" % (project.latitude, project.longitude),
            "created_at": project.created_at.to_datetime_string()
        }

        if es.exists(index=self.index, id=project.id, doc_type='projects'):
            es.update(index=self.index, id=project.id, doc_type='projects', body={"doc": project_doc})
        else:
            es.create(index=self.index, id=project.id, doc_type='projects', body=project_doc)

        es.indices.refresh(index=self.index)

        return True

    def delete_project_document(self, id):
        if es.exists(index=self.index, id=id, doc_type='projects'):
            es.delete(index=self.index, id=id, doc_type='projects')
            es.indices.refresh(index=self.index)

    def search_project(self):
        q = request.args.get('q', '')
        min_price = float_from_request('min_price', 0)
        max_price = float_from_request('max_price', 999999)
        published = bool_from_request('published', True)

        result = Search(using=es, index=self.index, doc_type='projects')
        if q:
            result = result.query("match_phrase", title=q) \
                .highlight('title')

        result = result.filter(Q('term', published=published)) \
            .filter('range', price={'gte': min_price, 'lte': max_price}) \
            .execute()
        return result.to_dict()

    def autocomplete_project(self):
        q = request.args.get('q', '')
        if not q:
            return self.get_empty_elastic_result()

        result = Search(using=es, index=self.index, doc_type='projects') \
                     .query("match", title=q) \
                     .highlight('title') \
                     .filter(Q('term', published=True))

        result = result[0:10].execute()

        return result.to_dict()

    def geo_search_project(self):
        published = bool(request.args.get('published', True))

        lat = float_from_request('lat', 0)
        lon = float_from_request('lon', 0)

        result = Search(using=es, index=self.index, doc_type='projects')

        try:
            result = result.filter(Q('term', published=published)) \
                .filter('geo_distance', distance="10km", location={"lat": lat, "lon": lon}) \
                .execute()
        except Exception as e:
            return self.get_empty_elastic_result()

        return result.to_dict()

    def get_empty_elastic_result(self):
        return {
            'hits': {
                'hits': [],
                'max_score': None,
                'total': 0
            }
        }
        # .sort('-price')
